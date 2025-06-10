# SolChain – Project Overview for AI Code Generators

## 🌟 Project Summary

SoulChain is a privacy-focused digital identity platform for refugees and stateless individuals, using AI and Solana blockchain. It allows users to generate secure, verifiable digital IDs using facial and voice biometrics.

---

## 🔧 Tech Stack

- **Backend**: Python, Flask
- **Frontend**: Tkinter (or optionally HTML)
- **AI Models**:
  - Face Recognition: OpenCV + dlib or FaceNet
  - Voice Embedding: HuggingFace Wav2Vec2
- **Blockchain**: Solana (smart contract in Rust)
- **Storage**: IPFS (via `ipfshttpclient`)
- **ZK Proofs** (Optional): Light Protocol / ZK libraries
- **Wallet**: Phantom wallet

---

## 🔁 Workflow Summary

1. **Registration**
   - User captures face + voice via Tkinter
   - Flask backend processes input
   - Extracts embeddings → hashes + encrypts
   - Encrypted blob uploaded to IPFS
   - IPFS CID and hash stored on Solana via smart contract

2. **Verification**
   - User scans face/voice
   - Backend re-generates embeddings
   - Verifies hash match with stored one on Solana
   - (Optionally uses ZK proof to verify without revealing raw data)

3. **User Output**
   - Receives QR Code or Phantom Wallet ID linked to digital ID
   - Identity can be verified without documents

---

## 📦 Key Modules to Implement

- `face_recognition.py`: Capture & process face embedding
- `voice_recognition.py`: Record voice & extract embedding
- `encryption.py`: AES encrypt/decrypt data
- `ipfs_utils.py`: Upload/download to IPFS
- `solana_utils.py`: Connect with Solana blockchain
- `qr_generator.py`: Create ID-linked QR code
- `main_ui.py`: Simple Tkinter GUI
- `lib.rs`: Solana program to store CID and identity hash

---

## 🔄 API Endpoints

- `POST /register` – Accept face/voice input and return QR/ID
- `POST /verify` – Accept new input, verify identity
- `GET /status/<wallet>` – Check if ID is active/valid

---

## 💬 Notes

- Biometric data is never stored directly on blockchain.
- Uses encryption + IPFS + Solana for decentralization.
- Designed with user privacy and humanitarian use-cases in mind.