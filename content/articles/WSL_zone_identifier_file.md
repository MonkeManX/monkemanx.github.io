---
title: "Prevent 'Zone.Identifier' Files in WSL"
date: 2024-11-04
tags: ["linux"]
---

If like me, you use WSL on Windows (yes, I know shame on me), you've probably encountered the issue where these annoying `Zone.Identifier` files are created whenever you download a file in Windows and copy it over to WSL.

These files are created as a security mechanism by Windows to signal that the file came from a different security zone, such as the internet.

There are supposedly multiple ways to prevent this. I'll list them here, try them all and pray one works.

## "Do Not Preserve Zone Information" Policy

You can disable the creation of these files as follows:
1. Press `Win + R` and type `gpedit.msc`.
2. Navigate to: User Configuration -> Administrative Templates -> Windows Components -> Attachment Manager.
3. Select the policy `Do not preserve zone information in file attachments`.
4. Set it to `Enabled`.

If you receive a message saying that `gpedit.msc` does not exist, like this:

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:50%" src="/attachments/gpeditmsc-error-introduction.png">
</figure>
{{< /rawhtml >}}

In that case, you can use the following script to enable it. Create a `.bat` file with the following content and run it as an administrator:

```bat
@echo off

pushd "%~dp0"

dir /b %SystemRoot%\servicing\Packages\Microsoft-Windows-GroupPolicy-ClientExtensions-Package~3*.mum >List.txt
dir /b %SystemRoot%\servicing\Packages\Microsoft-Windows-GroupPolicy-ClientTools-Package~3*.mum >>List.txt

for /f %%i in ('findstr /i . List.txt 2^>nul') do dism /online /norestart /add-package:"%SystemRoot%\servicing\Packages\%%i"

pause
```

I can’t guarantee anything about this script, I found it online(source provided below).

## Registry Method

You can also disable the creation of `.identifier` files via the Windows registry with the following command: `REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Attachments" /v SaveZoneInformation /t REG_DWORD /d 1 /f`. Again, no guarantees—found this in a GitHub issue.

## Set WSL and Windows to the Same Security Level

Go to Control Panel -> `Network and Internet` -> `Internet Options` -> `Security` -> `Local Intranet` -> `Sites` -> `Advanced`, and add `*.wsl.localhost` as a site.

{{< rawhtml >}}
<div style="display: flex; justify-content: center; gap: 20px;">
    <figure>
        <img style="display: block; margin: auto; width:80%;" src="/attachments/internet_prop_1.jpg">
    </figure>
    <figure>
        <img style="display: block; margin: auto; width:80%;" src="/attachments/internet_prop_2.jpg">
    </figure>
</div>
{{< /rawhtml >}}

This should align the security levels of WSL and Windows, preventing new `.Identifier` files from being created.

## The "I Gave Up" Method

If all else fails, just add the fucker to the `.gitignore` of your `git` projects.

## Conclusion

It seems this bug is quite old and likely won't be fixed anytime soon. Someday, I'll switch from Windows to a proper operating system.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:50%" src="/attachments/bug_comic.png">
    <figcaption style="text-align:center; margin-top: 10px;">
        The GitHub issue for this bug is quite entertaining to read, highly recommended.
    </figcaption>
</figure>
{{< /rawhtml >}}


---
Source:
- https://github.com/microsoft/WSL/issues/7456
- https://answers.microsoft.com/en-us/windows/forum/all/gpeditmsc-missing/cc1d05b2-457d-4aa6-839f-8136d0eddc35
- https://devblogs.microsoft.com/oldnewthing/20140311-00/?p=1543#:~:text=In%20the%20Group%20Policy%20editor,your%20computer%20even%20more%20dangerous
