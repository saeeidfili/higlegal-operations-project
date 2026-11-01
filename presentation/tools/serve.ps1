# Minimal static web server for Windows without Python or Node.
# Usage (from the repo root): powershell -ExecutionPolicy Bypass -File tools/serve.ps1 [-Port 8000]
param([string]$Root = (Split-Path -Parent $PSScriptRoot), [int]$Port = 8000)
$types = @{ ".html"="text/html; charset=utf-8"; ".css"="text/css"; ".js"="text/javascript"; ".json"="application/json"; ".png"="image/png"; ".jpg"="image/jpeg"; ".jpeg"="image/jpeg"; ".webp"="image/webp"; ".svg"="image/svg+xml"; ".woff2"="font/woff2"; ".gif"="image/gif"; ".mp4"="video/mp4" }
$rootFull = [IO.Path]::GetFullPath($Root)
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")
$listener.Start()
Write-Output "Serving $rootFull at http://localhost:$Port/  (Ctrl+C to stop)"
while ($listener.IsListening) {
  $ctx = $listener.GetContext()
  $rel = [Uri]::UnescapeDataString($ctx.Request.Url.AbsolutePath.TrimStart('/'))
  if ($rel -eq '') { $rel = 'index.html' }
  $full = [IO.Path]::GetFullPath((Join-Path $rootFull $rel))
  if ($full.StartsWith($rootFull) -and (Test-Path $full -PathType Container)) {
    if (-not $ctx.Request.Url.AbsolutePath.EndsWith('/')) {
      $ctx.Response.Redirect($ctx.Request.Url.AbsolutePath + '/' + $ctx.Request.Url.Query)
      $ctx.Response.Close()
      continue
    }
    $full = Join-Path $full 'index.html'
  }
  if ($full.StartsWith($rootFull) -and (Test-Path $full -PathType Leaf)) {
    $bytes = [IO.File]::ReadAllBytes($full)
    $ext = [IO.Path]::GetExtension($full).ToLower()
    if ($types.ContainsKey($ext)) { $ctx.Response.ContentType = $types[$ext] }
    $ctx.Response.Headers.Add("Cache-Control", "no-store")
    $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
  } else {
    $ctx.Response.StatusCode = 404
  }
  $ctx.Response.Close()
}
