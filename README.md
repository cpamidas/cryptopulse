# ⚡ CryptoPulse

**CryptoPulse** is a Python utility that monitors the "pulse" of the Ethereum network.  
It measures the number of pending transactions and analyzes the average gas price to indicate the current network state:

- 🔥 **HIGH** — network congestion, mempool exploding.
- 🟢 **NORMAL** — steady activity.
- 💤 **LOW** — calm state, transactions go through easily.

---

## 🚀 Installation & Usage

```bash
git clone https://github.com/username/cryptopulse.git
cd cryptopulse
pip install -r requirements.txt
python cryptopulse.py
