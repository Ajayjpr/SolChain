from flask import Flask, request, jsonify
from flask_cors import CORS
from ai.face_recognition import get_face_embedding
from ai.voice_recognition import get_voice_embedding
from utils.encryption import encrypt_data, decrypt_data
from blockchain.ipfs_utils import upload_to_ipfs, download_from_ipfs
from blockchain.solana_utils import store_identity_on_solana, verify_identity_on_solana
from utils.qr_generator import generate_qr_code
import hashlib
import os

app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['POST'])
def register():
    print("Received registration request")
    # 0. Check if request is multipart/form-data
    if not request.is_json and 'face' not in request.files and 'voice' not in request.files:
        return jsonify({'error': 'Invalid request format, expected multipart/form-data'}), 400
    print("Request format is valid, proceeding with registration")

    # # 1. Check if wallet address is provided
    # if 'wallet' not in request.form:
    #     return jsonify({'error': 'Wallet address is required'}), 400
    # print("Wallet address provided, proceeding with face and voice processing")
    # # 2. Check if face and voice files are provided

    print("Files:", request.files)
    print("Form data:", request.form)

    # 1. Receive face and voice data
    if 'face' not in request.files or 'voice' not in request.files:
        return jsonify({'error': 'Face and voice files required'}), 400
    
    face_file = request.files['face']
    voice_file = request.files['voice']
    face_bytes = face_file.read()
    voice_bytes = voice_file.read()

    # 2. Extract embeddings
    face_emb = get_face_embedding(face_bytes)
    voice_emb = get_voice_embedding(voice_bytes)
    if face_emb is None or voice_emb is None:
        return jsonify({'error': 'Failed to extract embeddings'}), 500

    # 3. Hash and encrypt
    combined = face_emb.tobytes() + voice_emb.tobytes()
    identity_hash = hashlib.sha256(combined).hexdigest()
    key = os.urandom(32)  # In production, use a user-specific key
    encrypted_blob = encrypt_data(combined, key)

    # 4. Upload to IPFS
    cid = upload_to_ipfs(encrypted_blob)
    if not cid:
        return jsonify({'error': 'Failed to upload to IPFS'}), 500

    # 5. Store CID and hash on Solana
    wallet_address = request.form.get('wallet', 'test_wallet')
    tx_hash = store_identity_on_solana(wallet_address, cid, identity_hash)

    # 6. Generate QR code (with wallet or CID)
    qr_img = generate_qr_code(wallet_address)
    # For demo, return just the CID and hash
    return jsonify({'cid': cid, 'identity_hash': identity_hash, 'tx_hash': tx_hash})

@app.route('/verify', methods=['POST'])
def verify():
    if 'face' not in request.files or 'voice' not in request.files:
        return jsonify({'error': 'Face and voice files required'}), 400
    face_file = request.files['face']
    voice_file = request.files['voice']
    face_bytes = face_file.read()
    voice_bytes = voice_file.read()

    # 2. Extract embeddings
    face_emb = get_face_embedding(face_bytes)
    voice_emb = get_voice_embedding(voice_bytes)
    if face_emb is None or voice_emb is None:
        return jsonify({'error': 'Failed to extract embeddings'}), 500

    # 3. Hash
    combined = face_emb.tobytes() + voice_emb.tobytes()
    identity_hash = hashlib.sha256(combined).hexdigest()
    wallet_address = request.form.get('wallet', 'test_wallet')
    verified = verify_identity_on_solana(wallet_address, identity_hash)
    return jsonify({'verified': bool(verified)})

@app.route('/status/<wallet>', methods=['GET'])
def status(wallet):
    # 1. Check if ID is active/valid for given wallet
    # For demo, just return active
    return jsonify({'wallet': wallet, 'status': 'active'})

if __name__ == '__main__':
    app.run(debug=True)
