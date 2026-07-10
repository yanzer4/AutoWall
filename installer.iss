#define AppName "AutoWall"
#define AppVersion "1.1.0"
#define AppPublisher "PlaylistTools"
#define AppExeName "AutoWall.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL=https://github.com/yanzer4/AutoWall
AppSupportURL=https://github.com/yanzer4/AutoWall/issues
DefaultDirName=C:\PlaylistTools\AutoWall
DefaultGroupName={#AppName}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputDir=installer_output
OutputBaseFilename=AutoWall_Setup_v{#AppVersion}
SetupIconFile=autowall.ico
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible
ShowLanguageDialog=auto

[Languages]
Name: "pt_BR"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "en";    MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Ícones adicionais:"; Flags: unchecked

[Files]
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "autowall.ico";        DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}";             Filename: "{app}\{#AppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\autowall.ico"
Name: "{group}\Desinstalar {#AppName}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#AppName}";     Filename: "{app}\{#AppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\autowall.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Iniciar {#AppName} agora"; Flags: postinstall skipifsilent nowait runascurrentuser
