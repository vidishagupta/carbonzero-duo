param(
    [string]$Text,
    [string]$OutputFile
)

Add-Type -AssemblyName System.Speech
$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speak.Rate = 0 # Normal speed
$speak.SetOutputToWaveFile($OutputFile)
$speak.Speak($Text)
$speak.Dispose()
Write-Host "Audio written to $OutputFile"
