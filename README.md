# carl-wealth-management

### Automating ```git pull``` for daily chart renders

1. ```code ~/Library/LaunchAgents/local.gitPullChartsCode.plist```
2. Paste the following and save:
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>local.gitPullChartsCode</string>
    <key>ProgramArguments</key>
    <array>
        <string>git</string>
        <string>-C</string>
        <string>/Users/jonathoncarl/projects/carl-wealth-management/</string>
        <string>pull</string>
    </array>
    <key>StandardErrorPath</key>
    <string>/tmp/local.gitPullChartsCode.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/local.gitPullChartsCode.out</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>18</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```
3.  Locate ```carl-wealth-management``` in Finder. Right click on ```carl-wealth-management```. At the bottom of the hover-options, find Services -> Folder Actions Setup.
4. Select **Run Service**, and **add a new item alert**. Make sure to enable **Folder Actions**.
5. At the command line, ```launchctl load ~/Library/LaunchAgents/local.gitPullChartsCode.plist```.
6. Git will not automatically pull each day at 6pm EST.
