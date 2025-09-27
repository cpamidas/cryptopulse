import time
import statistics
from web3 import Web3
from rich.console import Console
from rich.table import Table

console = Console()

class CryptoPulse:
    """
    CryptoPulse monitors Ethereum pending transactions (mempool) 
    and calculates a "pulse" score based on tx volume and gas price trends.
    """

    def __init__(self, rpc_url: str, window: int = 10):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.web3.is_connected():
            raise ConnectionError("❌ Failed to connect to RPC endpoint.")
        self.window = window
        self.pending_counts = []
        self.gas_prices = []

    def get_pending_stats(self):
        """
        Fetch pending transactions and extract counts and gas prices.
        """
        try:
            pending = self.web3.eth.get_block("pending", full_transactions=True)
            txs = pending.transactions
            count = len(txs)
            gas_prices = [tx.gasPrice for tx in txs if hasattr(tx, "gasPrice")]
            return count, gas_prices
        except Exception:
            return 0, []

    def update(self):
        """
        Update rolling stats window with the latest pending transactions.
        """
        count, gas_prices = self.get_pending_stats()
        self.pending_counts.append(count)
        self.gas_prices.extend(gas_prices)

        if len(self.pending_counts) > self.window:
            self.pending_counts.pop(0)
        if len(self.gas_prices) > self.window * 1000:  # limit memory
            self.gas_prices = self.gas_prices[-self.window * 1000:]

    def analyze(self):
        """
        Compute network pulse: average pending count, gas price, and qualitative state.
        """
        avg_count = statistics.mean(self.pending_counts) if self.pending_counts else 0
        avg_gas = statistics.mean(self.gas_prices) / 1e9 if self.gas_prices else 0
        pulse = "🔥 HIGH" if avg_count > 50000 else "🟢 NORMAL" if avg_count > 10000 else "💤 LOW"
        return avg_count, avg_gas, pulse

    def run(self, interval: int = 5):
        """
        Continuously monitor and display the Ethereum network pulse.
        """
        console.print("[bold green]CryptoPulse started...[/bold green]")
        while True:
            self.update()
            avg_count, avg_gas, pulse = self.analyze()

            table = Table(title="🌐 Ethereum Network Pulse")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="magenta")

            table.add_row("Avg pending tx", f"{avg_count:.0f}")
            table.add_row("Avg gas price (Gwei)", f"{avg_gas:.2f}")
            table.add_row("Pulse", pulse)

            console.clear()
            console.print(table)
            time.sleep(interval)


if __name__ == "__main__":
    # Example RPC: Infura, Alchemy, or your own node
    rpc_url = "https://eth-mainnet.g.alchemy.com/v2/demo"  
    cp = CryptoPulse(rpc_url=rpc_url, window=12)
    cp.run(interval=6)
