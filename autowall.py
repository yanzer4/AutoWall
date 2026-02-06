from tkinter import messagebox
import subprocess
import ctypes
import sys
import re
import unicodedata
import customtkinter as ctk

# =============================
# CONFIGURAÇÕES FIXAS DO APP
# =============================
PROFILES = "Domain,Private,Public"
APP_TITLE = "AUTOWALL - Gerenciador de Firewall"
MAX_INTERNAL_BASE_LEN = 32
MIN_PORT = 1
MAX_PORT = 65535

THEME_BG = "#f4f6fb"
CARD_BG = "#ffffff"
TEXT_PRIMARY = "#1f2937"
TEXT_SECONDARY = "#4b5563"
ACCENT = "#0f766e"
ACCENT_HOVER = "#115e59"

# =============================
# VERIFICA SE É ADMINISTRADOR
# =============================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# =============================
# EXECUTA COMANDO POWERSHELL
# =============================
def run_powershell(command: str):
    result = subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True
    )
    error_output = (result.stderr or "").strip()
    if not error_output:
        error_output = (result.stdout or "").strip()
    return result.returncode, error_output


def is_valid_rule_char(char: str) -> bool:
    return char.isalnum() or char in {" ", "_", "-"}


def collect_invalid_characters(value: str) -> dict[str, int]:
    invalid_characters = {}
    for char in value:
        if not is_valid_rule_char(char):
            invalid_characters[char] = invalid_characters.get(char, 0) + 1
    return invalid_characters


def format_invalid_character(char: str, count: int) -> str:
    special_labels = {
        "\t": "<TAB>",
        "\n": "<LF>",
        "\r": "<CR>",
    }
    label = special_labels.get(char, f'"{char}"')
    code = f"U+{ord(char):04X}"
    if count > 1:
        return f"{label} - {code} (x{count})"
    return f"{label} - {code}"


def parse_ports_input(value: str) -> tuple[str | None, list[str]]:
    raw_items = value.split(",")
    errors = []
    valid_items = []

    for raw_item in raw_items:
        item = raw_item.strip()
        if not item:
            errors.append("(vazio): item vazio entre virgulas")
            continue

        if "-" in item:
            if item.count("-") != 1:
                errors.append(f"{item}: formato inválido")
                continue

            start_text, end_text = item.split("-")
            if not start_text.isdigit() or not end_text.isdigit():
                errors.append(f"{item}: formato inválido")
                continue

            start_port = int(start_text)
            end_port = int(end_text)

            if start_port < MIN_PORT or start_port > MAX_PORT:
                errors.append(f"{item}: porta inicial fora do limite ({MIN_PORT}-{MAX_PORT})")
                continue

            if end_port < MIN_PORT or end_port > MAX_PORT:
                errors.append(f"{item}: porta final fora do limite ({MIN_PORT}-{MAX_PORT})")
                continue

            if start_port > end_port:
                errors.append(f"{item}: intervalo invertido")
                continue

            valid_items.append(f"{start_port}-{end_port}")
            continue

        if not item.isdigit():
            errors.append(f"{item}: formato inválido")
            continue

        port = int(item)
        if port < MIN_PORT or port > MAX_PORT:
            errors.append(f"{item}: fora do limite ({MIN_PORT}-{MAX_PORT})")
            continue

        valid_items.append(str(port))

    if errors:
        return None, errors

    return ",".join(valid_items), []


def sanitize_internal_base_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^A-Za-z0-9_-]", "_", ascii_value)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_-")
    if not cleaned:
        cleaned = "REGRA"
    return cleaned[:MAX_INTERNAL_BASE_LEN]

# =============================
# CRIA AS REGRAS DE FIREWALL
# =============================
def create_firewall_rules():
    rule_name_raw = entry_rule_name.get().strip()
    ports_raw = entry_ports.get().strip()

    if not rule_name_raw:
        messagebox.showwarning(
            "Campo obrigatório",
            "Informe um nome para a regra."
        )
        entry_rule_name.focus_set()
        return

    if not ports_raw:
        messagebox.showwarning(
            "Campo obrigatório",
            "Informe ao menos uma porta ou intervalo de portas."
        )
        entry_ports.focus_set()
        return

    local_ports, port_errors = parse_ports_input(ports_raw)
    if port_errors:
        messagebox.showerror(
            "Portas inválidas",
            "Corrija o campo Porta(s) para continuar.\n\n"
            "Itens inválidos encontrados:\n"
            + "\n".join(f"- {item}" for item in port_errors)
        )
        entry_ports.focus_set()
        entry_ports.select_range(0, "end")
        return

    invalid_characters = collect_invalid_characters(rule_name_raw)
    if invalid_characters:
        details = "\n".join(
            format_invalid_character(char, count)
            for char, count in invalid_characters.items()
        )
        messagebox.showerror(
            "Caracteres inválidos",
            "O nome informado contém caracteres inválidos.\n"
            "Corrija o campo para continuar.\n\n"
            "Códigos inválidos encontrados:\n"
            f"{details}"
        )
        entry_rule_name.focus_set()
        entry_rule_name.select_range(0, "end")
        return

    rule_name_display = rule_name_raw
    rule_name_internal = sanitize_internal_base_name(rule_name_raw)

    rule_specs = [
        ("TCP Entrada", "Inbound", "TCP", "TCP_IN"),
        ("TCP Saída", "Outbound", "TCP", "TCP_OUT"),
        ("UDP Entrada", "Inbound", "UDP", "UDP_IN"),
        ("UDP Saída", "Outbound", "UDP", "UDP_OUT"),
    ]

    rules = []
    for label, direction, protocol, suffix in rule_specs:
        display_name = f"{rule_name_display} - {label}"
        internal_name = f"AUTOWALL_{rule_name_internal}_{suffix}"
        command = (
            f'New-NetFirewallRule -Name "{internal_name}" '
            f'-DisplayName "{display_name}" '
            f'-Direction {direction} -Protocol {protocol} '
            f'-LocalPort {local_ports} -Action Allow -Profile {PROFILES} '
            f'-ErrorAction Stop'
        )
        rules.append((display_name, command))

    errors = []

    for display_name, rule in rules:
        code, err = run_powershell(rule)
        if code != 0:
            detail = err if err else "Erro desconhecido."
            errors.append(f"{display_name}: {detail}")

    if errors:
        messagebox.showerror(
            "Erro ao criar regras",
            "Algumas regras não puderam ser criadas:\n\n" +
            "\n".join(errors)
        )
    else:
        messagebox.showinfo(
            "Sucesso",
            "Regras TCP e UDP criadas com sucesso!\n\n"
            f"Nome base aplicado: {rule_name_display}\n"
            f"Porta(s): {local_ports}"
        )

# =============================
# BLOQUEIA EXECUÇÃO SEM ADMIN
# =============================
if not is_admin():
    messagebox.showerror(
        "Permissão necessária",
        "O AUTOWALL precisa ser executado como ADMINISTRADOR."
    )
    sys.exit(0)

# =============================
# INTERFACE GRÁFICA
# =============================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title(APP_TITLE)
root.geometry("620x460")
root.resizable(False, False)
root.configure(fg_color=THEME_BG)

frame = ctk.CTkFrame(
    root,
    fg_color=CARD_BG,
    corner_radius=14,
    border_width=1,
    border_color="#dbe2ea",
)
frame.pack(fill="both", expand=True, padx=24, pady=24)

title_label = ctk.CTkLabel(
    frame,
    text="Nome base da regra",
    text_color=TEXT_PRIMARY,
    font=("Segoe UI Semibold", 18),
)
title_label.pack(anchor="w", padx=24, pady=(20, 8))

entry_rule_name = ctk.CTkEntry(
    frame,
    height=38,
    corner_radius=10,
    border_color="#cfd8e3",
    fg_color="#f8fafc",
    text_color=TEXT_PRIMARY,
    font=("Segoe UI", 14),
    placeholder_text="Ex.: Regra Financeiro-3030",
)
entry_rule_name.pack(fill="x", padx=24, pady=(0, 14))

ports_label = ctk.CTkLabel(
    frame,
    text="Porta(s)",
    text_color=TEXT_PRIMARY,
    font=("Segoe UI Semibold", 14),
)
ports_label.pack(anchor="w", padx=24, pady=(0, 6))

entry_ports = ctk.CTkEntry(
    frame,
    height=38,
    corner_radius=10,
    border_color="#cfd8e3",
    fg_color="#f8fafc",
    text_color=TEXT_PRIMARY,
    font=("Segoe UI", 14),
    placeholder_text="Ex.: 8080, 8443, 3030-3040",
)
entry_ports.pack(fill="x", padx=24, pady=(0, 14))

info_label = ctk.CTkLabel(
    frame,
    text=(
        "O AUTOWALL criará automaticamente:\n"
        "- Regras TCP e UDP\n"
        "- Entrada e Saída\n"
        "- Porta única ou intervalo\n"
        "- Múltiplas entradas separadas por vírgula\n"
        "- Perfis Domínio, Privado e Público\n"
        "- Validação de caracteres"
    ),
    justify="left",
    anchor="w",
    text_color=TEXT_SECONDARY,
    font=("Segoe UI", 13),
)
info_label.pack(fill="x", padx=24, pady=(0, 18))

btn_create = ctk.CTkButton(
    frame,
    text="Criar regras no Firewall",
    height=44,
    corner_radius=12,
    fg_color=ACCENT,
    hover_color=ACCENT_HOVER,
    text_color="#ffffff",
    font=("Segoe UI Semibold", 14),
    command=create_firewall_rules,
)
btn_create.pack(fill="x", padx=24, pady=(0, 22))

entry_rule_name.focus_set()

root.mainloop()
