<#
.SYNOPSIS
Resolves Unity package dependencies across platforms
#>

param(
    [string]$Platform,
    [string]$BuildNumber
)

$manifest = Get-Content "Packages/manifest.json" | ConvertFrom-Json

# Platform-specific overrides
switch ($Platform) {
    "Android" {
        $manifest.dependencies["com.unity.mobile.android-logger"] = "2.1.0"
        $manifest.dependencies["com.unity.ads"] = "4.4.1"
    }
    "iOS" {
        $manifest.dependencies["com.unity.mobile.iOS-support"] = "1.0.0"
        $manifest.dependencies["com.unity.ads"] = "4.3.0" # Different version for iOS
    }
}

# Apply build-specific patches
if ($BuildNumber -gt "2024.03.00") {
    $manifest.dependencies["com.unity.analytics"] = "3.5.2"
}

# Save updated manifest
$manifest | ConvertTo-Json -Depth 10 | Out-File "Packages/manifest.json"