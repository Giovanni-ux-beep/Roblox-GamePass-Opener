import tkinter as tk
from tkinter import messagebox
from urllib.parse import urlparse
import webbrowser

ROBLOX_HOSTS = {
    "roblox.com",
    "www.roblox.com",
    "create.roblox.com",
}


def is_valid_roblox_url(value: str) -> bool:
    value = value.strip()
    if not value:
        return False

    candidate = value if "://" in value else "https://" + value

    try:
        parsed = urlparse(candidate)
    except ValueError:
        return False

    host = (parsed.hostname or "").lower()
    return host in ROBLOX_HOSTS and parsed.scheme in ("http", "https") and bool(parsed.path)


def normalize_url(value: str) -> str:
    value = value.strip()
    return value if "://" in value else "https://" + value


def open_gamepass():
    raw_url = url_var.get().strip()

    if not is_valid_roblox_url(raw_url):
        status_var.set("❌ URL no válida")
        messagebox.showerror(
            "URL no válida",
            "Pegá una URL válida de Roblox, por ejemplo:\n"
            "https://www.roblox.com/game-pass/..."
        )
        return

    url = normalize_url(raw_url)

    confirmed = messagebox.askokcancel(
        "Confirmar Game Pass",
        "Vas a abrir esta dirección:\n\n"
        f"{url}\n\n"
        "Revisá que sea el Game Pass correcto.\n"
        "El programa no realizará la compra."
    )

    if not confirmed:
        status_var.set("Operación cancelada.")
        return

    webbrowser.open(url)
    status_var.set("✓ Game Pass abierto en el navegador.")


def clear_url():
    url_var.set("")
    status_var.set("Esperando URL...")
    url_entry.focus_set()


root = tk.Tk()
root.title("Roblox Game Pass Opener")
root.geometry("680x300")
root.resizable(False, False)

frame = tk.Frame(root, padx=28, pady=24)
frame.pack(fill="both", expand=True)

title = tk.Label(
    frame,
    text="ROBLOX GAME PASS OPENER",
    font=("Segoe UI", 18, "bold")
)
title.pack(pady=(0, 18))

subtitle = tk.Label(
    frame,
    text="Abrí rápidamente un Game Pass para realizar la compra manualmente.",
    font=("Segoe UI", 10)
)
subtitle.pack(pady=(0, 15))

tk.Label(
    frame,
    text="Game Pass URL:",
    font=("Segoe UI", 10, "bold"),
    anchor="w"
).pack(fill="x")

url_var = tk.StringVar()
url_entry = tk.Entry(frame, textvariable=url_var, font=("Segoe UI", 11))
url_entry.pack(fill="x", ipady=7, pady=(6, 14))
url_entry.focus_set()

button_frame = tk.Frame(frame)
button_frame.pack()

tk.Button(
    button_frame,
    text="ABRIR GAME PASS",
    command=open_gamepass,
    font=("Segoe UI", 10, "bold"),
    padx=18,
    pady=8
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="LIMPIAR",
    command=clear_url,
    font=("Segoe UI", 10),
    padx=18,
    pady=8
).pack(side="left", padx=5)

status_var = tk.StringVar(value="Esperando URL...")
tk.Label(
    frame,
    textvariable=status_var,
    font=("Segoe UI", 10),
    anchor="w"
).pack(fill="x", pady=(20, 0))

tk.Label(
    frame,
    text="El programa no guarda credenciales, cookies ni tokens y no realiza compras.",
    font=("Segoe UI", 9)
).pack(pady=(8, 0))

root.bind("<Return>", lambda event: open_gamepass())
root.mainloop()
