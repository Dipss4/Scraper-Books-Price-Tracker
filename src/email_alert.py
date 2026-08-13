"""
V6 — Send email alerts.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rich.console import Console

from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASS
from price_history import get_price_history

console = Console()


def build_history_table(title: str) -> str:
    entries = get_price_history(title)
    if not entries:
        return "<p>No price history available.</p>"

    rows = ""
    for entry in entries[-10:]:
        rows += (
            f'<tr>'
            f'<td style="padding:6px 12px;border:1px solid #ddd;">{entry["date"]}</td>'
            f'<td style="padding:6px 12px;border:1px solid #ddd;text-align:center;">'
            f'£{entry["price"]:.2f}</td>'
            f'</tr>'
        )

    return (
        f'<table style="border-collapse:collapse;font-family:Arial;">'
        f'<thead><tr style="background:#f2f2f2;">'
        f'<th style="padding:8px 12px;border:1px solid #ddd;">Date</th>'
        f'<th style="padding:8px 12px;border:1px solid #ddd;">Price</th>'
        f'</tr></thead>'
        f'<tbody>{rows}</tbody></table>'
    )


def build_email_html(alert: dict) -> str:
    history_table = build_history_table(alert["title"])

    return f"""
    <html><body style="font-family:Arial;color:#333;">
    <div style="max-width:600px;margin:auto;padding:20px;border:1px solid #ddd;border-radius:8px;">
        <h2 style="color:#e74c3c;">🔔 Price Drop Alert!</h2>
        <table style="width:100%;border-collapse:collapse;margin:16px 0;">
            <tr><td style="padding:8px;background:#f9f9f9;font-weight:bold;">Book</td>
                <td style="padding:8px;">{alert['title']}</td></tr>
            <tr><td style="padding:8px;background:#f9f9f9;font-weight:bold;">Old Price</td>
                <td style="padding:8px;color:#888;">£{alert['old_price']:.2f}</td></tr>
            <tr><td style="padding:8px;background:#f9f9f9;font-weight:bold;">New Price</td>
                <td style="padding:8px;color:#27ae60;font-size:1.2em;">
                <strong>£{alert['new_price']:.2f}</strong></td></tr>
            <tr><td style="padding:8px;background:#f9f9f9;font-weight:bold;">You Save</td>
                <td style="padding:8px;color:#e74c3c;">
                £{alert['drop']:.2f} ({alert['drop_pct']:.1f}%)</td></tr>
            <tr><td style="padding:8px;background:#f9f9f9;font-weight:bold;">Target</td>
                <td style="padding:8px;">£{alert['target_price']:.2f}</td></tr>
        </table>
        <h3>📈 Price History</h3>
        {history_table}
        <br><p style="color:#888;font-size:0.85em;">— Books Price Tracker</p>
    </div></body></html>
    """


def send_alert_email(alert: dict):
    if not SENDER_EMAIL or not SENDER_PASS:
        console.print("[yellow]⚠ SMTP not configured. Skipping email.[/]")
        console.print(f"[dim]  Would alert {alert['email']} about '{alert['title']}'[/]")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🔔 Price Drop: {alert['title'][:50]}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = alert["email"]

    plain = (
        f"Price Drop!\n"
        f"Book: {alert['title']}\n"
        f"Was: £{alert['old_price']:.2f} → Now: £{alert['new_price']:.2f}\n"
        f"Save: £{alert['drop']:.2f} ({alert['drop_pct']:.1f}%)\n"
    )

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(build_email_html(alert), "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASS)
            server.sendmail(SENDER_EMAIL, alert["email"], msg.as_string())
            console.print(f"[green]✓ Email sent to {alert['email']}[/]")
    except smtplib.SMTPAuthenticationError:
        console.print("[red]✗ SMTP auth failed. Check .env credentials.[/]")
    except Exception as e:
        console.print(f"[red]✗ Email error: {e}[/]")


def send_all_alerts(alerts: list):
    if not alerts:
        console.print("[dim]No alerts to send.[/]")
        return

    console.print(f"\n[bold]Sending {len(alerts)} alert(s)...[/]")
    for alert in alerts:
        send_alert_email(alert)