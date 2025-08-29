$sessionXmlPath = "C:\dcloud\session.xml"
$podsConfigPath = "C:\Scripts\pods.txt"
$remoteCommand1 = "diskspd.exe -c40G -b1M -d300 -r -w90 -t8 -o256 -Sh -L -Zr -W0 E:\san_testfile_small.dat"
$remoteCommand2 = "diskspd.exe -c40G -b1M -d300 -r -w10 -t8 -o256 -Sh -L -Zr -W0 E:\san_testfile_large.dat"

try {
    if (-not (Test-Path $sessionXmlPath)) {
        throw "Session XML file not found at: $sessionXmlPath"
    }
    if (-not (Test-Path $podsConfigPath)) {
        throw "Pods configuration file not found at: $podsConfigPath"
    }

    $xmlContent = Get-Content $sessionXmlPath -Raw
    $match = [regex]::Match($xmlContent, '(dcv-mds-pod\d+)')

    if (-not $match.Success) {
        throw "Could not find a valid pod name (e.g., dcv-mds-pod1) in $sessionXmlPath"
    }
    $currentPodName = $match.Groups[1].Value

    $settings = @{}
    Get-Content $podsConfigPath | ForEach-Object {
        if ($_ -match '^\s*#' -or -not $_.Trim()) { return }
        $key, $value = $_.Split('=', 2)
        if ($key -and $value) { $settings[$key.Trim()] = $value.Trim() }
    }

    $targetIp = $settings[$currentPodName]
    $username = $settings['Username']
    $password = $settings['Password']

    if (-not $targetIp) { throw "IP address for '$currentPodName' not found in $podsConfigPath." }
    if (-not $username) { throw "Username not found in $podsConfigPath." }
    if (-not $password) { throw "Password not found in $podsConfigPath." }

    $securePassword = ConvertTo-SecureString -String $password -AsPlainText -Force
    $credential = New-Object System.Management.Automation.PSCredential($username, $securePassword)

    $session = New-PSSession -ComputerName $targetIp -Credential $credential -ErrorAction Stop
    
    Invoke-Command -Session $session -ScriptBlock {
        param($cmd1, $cmd2)

        Write-Host "
##################################################################
# The script is now running and will complete in 5 minutes.      #
# Please do not close this window until the process is complete. #
# Only one script can be run at a time.                          #
##################################################################"

        $job1 = Start-Job -ScriptBlock { 
            param($command)
            cmd.exe /c $command 
        } -ArgumentList $cmd1

        $job2 = Start-Job -ScriptBlock { 
            param($command)
            cmd.exe /c $command
        } -ArgumentList $cmd2

        Wait-Job -Job $job1, $job2
        Receive-Job -Job $job1, $job2
        Remove-Job -Job $job1, $job2
    } -ArgumentList $remoteCommand1, $remoteCommand2
}
catch {
    Write-Error "An error occurred: $($_.Exception.Message)"
}
finally {
    if ($session) {
        Remove-PSSession -Session $session
    }
}

Read-Host "Press Enter to exit..."
