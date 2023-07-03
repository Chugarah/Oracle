# Test

Yarn requires Node.js 4 or higher to be installed.

```powershell
npm install --global yarn
yarn setup
```

Yarn setup will fail to create, copy our env. We need to do this manually

```powershell
Copy-Item -Path ./server/.env.example -Destination ./server/.env.development -Force
Copy-Item -Path ./collector/.env.example -Destination ./collector/.env -Force
Copy-Item -Path ./docker/.env.example -Destination ./docker/.env -Force
Write-Host "All ENV files copied!"
```

Now fill in the environment file with the proper values.