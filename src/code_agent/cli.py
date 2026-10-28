import typer
from rich.console import Console
from .llm import LLMClient

app = typer.Typer(help="Mini Code Agent - 本地代码智能助手")
console = Console()
llm_client = LLMClient()

@app.command()
def ask(question: str = typer.Argument(..., help="要提问的问题")):
    console.print("[bold blue]正在思考中...[/bold blue]")
    try:
        answer = llm_client.chat(question)
        console.print("\n[bold green]总结：[/bold green]", answer.summary)
        console.print("\n[bold green]详细内容：[/bold green]")
        console.print(answer.content)
    except RuntimeError as e:
        console.print(f"[bold red]错误：[/bold red] {e}", err=True)
        raise typer.Exit(code=1)

def main():
    app()

if __name__ == "__main__":
    main()
