Get-Content ..\.env | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -match '^\s*$') {
        return
    }

    $name, $value = $_ -split '=', 2
    if ($name -and $value) {
        [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), "Process")
    }
}

& ..\.venv\Scripts\dbt.exe @args --project-dir . --profiles-dir .dbt
