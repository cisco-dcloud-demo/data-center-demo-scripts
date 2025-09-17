$sessionXmlPath = "C:\dcloud\session.xml"
$podsFilePath = "C:\Scripts\pods.txt"
$remoteCommand1 = "diskspd.exe -c35G -b1M -d300 -r -w99 -t8 -o64 -L -Sh -L -Zr -W0 E:\san_testfile_small.dat"
$remoteCommand2 = "diskspd.exe -c35G -b8k -d300 -r -w99 -t16 -o256 -L -Sh -L -Zr -W0 E:\san_testfile_large.dat"

$settings = @{
    "dcv-mds-pod1" = "198.19.253.171"
    "dcv-mds-pod2" = "198.19.253.172"
    "dcv-mds-pod3" = "198.19.253.173"
    "dcv-mds-pod4" = "198.19.253.174"
    "dcv-mds-pod5" = "198.19.253.175"
    "dcv-mds-pod6" = "198.19.253.181"
    "dcv-mds-pod7" = "198.19.253.177"
    "dcv-mds-pod8" = "198.19.253.178"
}

try {
    if (-not (Test-Path $sessionXmlPath)) {
        throw "Session XML file not found at: $sessionXmlPath"
    }

    if (-not (Test-Path $podsFilePath)) {
        throw "Credentials file not found at: $podsFilePath"
    }

    $xmlContent = Get-Content $sessionXmlPath -Raw
    $match = [regex]::Match($xmlContent, '(dcv-mds-pod\d+)')

    if (-not $match.Success) {
        throw "Could not find a valid pod name (e.g., dcv-mds-pod1) in $sessionXmlPath"
    }
    $currentPodName = $match.Groups[1].Value

    $targetIp = $settings[$currentPodName]
    if (-not $targetIp) {
        throw "IP address for '$currentPodName' not found in the script's configuration."
    }

    $fileLines = Get-Content -Path $podsFilePath

    $usernameLine = $fileLines | Where-Object { $_ -match '^Username=' }
    $passwordLine = $fileLines | Where-Object { $_ -match '^Password=' }

    if (-not $usernameLine -or -not $passwordLine) {
        throw "Username or Password not found in $podsFilePath"
    }

    $username = $usernameLine -replace '^Username=', ''
    $password = $passwordLine -replace '^Password=', ''

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
