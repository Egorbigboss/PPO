;------------------------------------------------------------------------------
;
;       ������ ������������� ������� ��� Inno Setup 5.5.5
;       (c) maisvendoo, 15.04.2015
;
;------------------------------------------------------------------------------

;------------------------------------------------------------------------------
;   ���������� ��������� ���������
;------------------------------------------------------------------------------

; ��� ����������
#define   Name       "GPX View"
; ������ ����������
#define   Version    "0.7.0beta"
; �����-�����������
#define   Publisher  "Egor"
; ���� ����� ������������
;#define   URL        "http://www.miramishi.com"
; ��� ������������ ������
;#define   ExeName    "Miramishi.exe"


[Setup]

; ���������� ������������� ����������,
;��������������� ����� Tools -> Generate GUID
AppId={{A3C402FC-50FD-4978-8C82-008860FCDAA9}

 ; ������ ����������, ������������ ��� ���������
AppName={#Name}
AppVersion={#Version}
AppPublisher={#Publisher}
;AppPublisherURL={#URL}
;AppSupportURL={#URL}
;AppUpdatesURL={#URL}

; ���� ��������� ��-���������
DefaultDirName={pf}\{#Name}
; ��� ������ � ���� "����"
DefaultGroupName={#Name}

; �������, ���� ����� ������� ��������� setup � ��� ������������ �����
OutputDir=C:\Users\Egor\Documents\Visual Studio 2015\Projects\PPO1\PPO1
OutputBaseFileName=test-setup


 ; ���� ������
;SetupIconFile=E:\work\Mirami\Mirami\icon.ico

; ��������� ������
Compression=lzma
SolidCompression=yes

;------------------------------------------------------------------------------
;   ������������� ����� ��� �������� ���������
;------------------------------------------------------------------------------
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl";
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl";



;------------------------------------------------------------------------------
;   �����, ������� ���� �������� � ����� �����������
;------------------------------------------------------------------------------
[Files]

; ����������� ����
Source: "C:\Users\Egor\Documents\Visual Studio 2015\Projects\PPO1\PPO1\GPX Viewer.bat"; DestDir: "{app}"; Flags: ignoreversion
; ������������� �������
Source: "C:\Users\Egor\Documents\Visual Studio 2015\Projects\PPO1\PPO1\command.py"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Egor\Documents\Visual Studio 2015\Projects\PPO1\PPO1\main.py"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Egor\Documents\Visual Studio 2015\Projects\PPO1\PPO1\parser_gpx.py"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Egor\Documents\Visual Studio 2015\Projects\PPO1\PPO1\interface.py"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Egor\Documents\Visual Studio 2015\Projects\PPO1\PPO1\plotter.py"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Egor\Documents\Visual Studio 2015\Projects\PPO1\PPO1\engine.py"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Egor\Documents\Visual Studio 2015\Projects\PPO1\PPO1\service.bat"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Egor\Documents\Visual Studio 2015\Projects\PPO1\PPO1\python-3.6.4.exe"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs


[Run]
Filename: "{app}\service.bat";
