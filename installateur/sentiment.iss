; Script Inno Setup pour sentiment-app 1.0.0
; Genere par le projet sentiment-app (A. Larhlimi)

#define AppVersion "1.0.0"
#define AppName "sentiment-app"
#define AppPublisher "A. Larhlimi"
#define AppExeName "sentiment.cmd"

[Setup]
AppId={{F3A2B1C4-7D8E-4F9A-B2C3-D4E5F6A7B8C9}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL=https://github.com/AYOUB185/sentiment-app
AppSupportURL=https://github.com/AYOUB185/sentiment-app
AppUpdatesURL=https://github.com/AYOUB185/sentiment-app/releases
DefaultDirName={localappdata}\Programs\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
; Installation sans droits administrateur
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=Output
OutputBaseFilename=sentiment-app-{#AppVersion}-setup
SetupIconFile=
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
; Langue francaise
ShowLanguageDialog=no

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "modifypath"; Description: "Ajouter {#AppName} au PATH de l'utilisateur (recommande)"; GroupDescription: "Options :"; Flags: checked

[Files]
; Tout le contenu de build\app\
Source: "build\app\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Analyser un avis"; Filename: "{cmd}"; Parameters: "/k ""{app}\sentiment.cmd"" --help"; WorkingDir: "{app}"
Name: "{group}\Desinstaller {#AppName}"; Filename: "{uninstallexe}"

[Registry]
; Ajout au PATH utilisateur si la tache est cochee
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: NeedsAddPath(ExpandConstant('{app}')); Tasks: modifypath

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', OrigPath) then
  begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Uppercase(Param) + ';', ';' + Uppercase(OrigPath) + ';') = 0;
end;

[UninstallReg]
; Retirer du PATH a la desinstallation
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{code:RemovePath|{app}}"

[Code]
function RemovePath(Param: string): string;
var
  OrigPath: string;
  P: Integer;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', OrigPath) then
  begin
    Result := '';
    exit;
  end;
  P := Pos(';' + Uppercase(Param), ';' + Uppercase(OrigPath));
  if P = 0 then
    Result := OrigPath
  else
    Delete(OrigPath, P - 1, Length(Param) + 1);
  Result := OrigPath;
end;

