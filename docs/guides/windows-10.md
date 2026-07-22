# Windows 10

## Disable Activity History

https://support.microsoft.com/windows/privacy/windows-activity-history-and-your-privacy

1. As admin, in `cmd`:
    ```batch
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" /v "PublishUserActivities" /t REG_DWORD /d 0 /f
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" /v "EnableActivityFeed" /t REG_DWORD /d 0 /f
    reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" /v "UploadUserActivities" /t REG_DWORD /d 0 /f
    ```
2. Log out and log in to apply.

## Disable Optional Hardware Apps

1. Open `System Properties`: `sysdm.cpl`
2. Switch to the `Hardware` tab.
3. Open `Device Installation Settings`.
4. Disable automatic download.
