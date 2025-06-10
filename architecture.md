# SoulChain – Project Architecture and Directory Structure

## 📐 System Architecture

+---------------------------+
| User Frontend (Tkinter) |
+---------------------------+
|
v
+---------------------------+
| Flask Backend (API Server)|
+---------------------------+
| - Handles requests |
| - Captures image/audio |
| - Extracts embeddings |
| - Encrypts data |
| - Uploads to IPFS |
| - Interacts with Solana |
+---------------------------+
|
v
+-----------------------------+
| IPFS Decentralized Storage |
+-----------------------------+
|
v
+---------------------------+
| Solana Smart Contract |
+---------------------------+
| - Stores IPFS CID |
| - Stores user hash |
| - Optionally handles ZK |
+---------------------------+

yaml
Copy
Edit

---

## 🗂 Directory Structure

soulchain/
├── backend/
│ ├── app.py # Flask API endpoints
│ ├── ai/
│ │ ├── face_recognition.py
│ │ └── voice_recognition.py
│ ├── blockchain/
│ │ ├── solana_utils.py # Interact with Solana
│ │ └── ipfs_utils.py # Upload/download from IPFS
│ └── utils/
│ ├── encryption.py
│ └── qr_generator.py
├── frontend/
│ └── main_ui.py # Tkinter UI
├── smart_contract/
│ └── src/
│ └── lib.rs # Rust Solana program
├── tests/
│ └── test_api.py
├── requirements.txt
└── README.md