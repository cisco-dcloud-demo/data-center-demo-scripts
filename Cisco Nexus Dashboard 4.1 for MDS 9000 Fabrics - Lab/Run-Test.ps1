$computerName = "198.19.253.174"
$userName = "dcloud\demouser"
$plainTextPassword = "C1sco12345"

$securePassword = ConvertTo-SecureString -String $plainTextPassword -AsPlainText -Force

$credential = New-Object System.Management.Automation.PSCredential($userName, $securePassword)

$scriptBlock = {
    cmd /c "diskspd.exe -c40G -b1M -d10 -r -w100 -t8 -o64 -L -Sh -L -Zr -W0 E:\san_testfile_small.dat"
    cmd /c "diskspd.exe -c40G -b8k -d10 -r -w10 -t16 -o256 -L -Sh -L -Zr -W0 E:\san_testfile_large.dat"
}

Write-Host "Starting remote disk tests on $computerName..."
Invoke-Command -ComputerName $computerName -Credential $credential -ScriptBlock $scriptBlock

Write-Host "Remote commands have been launched successfully."
Read-Host "Press ENTER to exit."
