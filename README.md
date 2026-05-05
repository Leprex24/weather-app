# Zadanie 1 – Część nieobowiązkowa

## Punkt 1 – Obraz multiplatformowy (linux/amd64 i linux/arm64)

### Utworzenie buildera opartego na sterowniku docker-container

Stworzenie nowego buildera o nazwie `multibuilder` opartego na sterowniku `docker-container`:
```angular2html
docker buildx create --name multibuilder --driver docker-container --bootstrap
```
Przełączenie się na nowo utworzony builder:
```angular2html
docker buildx use multibuilder
```
Weryfikacja czy builder działa i obsługuje obie platformy:
```angular2html
PS C:\Studia\chmura\chmura_zad1> docker buildx inspect multibuilder
Name:          multibuilder
Driver:        docker-container
Last Activity: 2026-05-05 16:34:40 +0000 UTC

Nodes:
Name:                  multibuilder0
Endpoint:              desktop-linux
Status:                running
BuildKit daemon flags: --allow-insecure-entitlement=network.host
BuildKit version:      v0.29.0
Platforms:             linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/arm64, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/arm/v7, linux/arm/v6
```
### Budowanie i publikacja obrazu na DockerHub

Budowanie obrazu dla obu platform i pushowanie do repozytorium na DockerHub:
```angular2html
docker buildx build --platform linux/amd64,linux/arm64 -t leprex24/pawcho-sawicki:weather-app.v.1.0 --push .
```
### Weryfikacja manifestu

Sprawdzenie czy manifest zawiera deklaracje dla obu platform:
```angular2html
PS C:\Studia\chmura\chmura_zad1> docker buildx imagetools inspect leprex24/pawcho-sawicki:weather-app.v.1.0
Name:      docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0
MediaType: application/vnd.oci.image.index.v1+json
Digest:    sha256:ab2d5f34eaf591c0db9c04c3e42190bb742727517d975621398b6c1dd276d6c3

Manifests:
  Name:        docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0@sha256:85f9517c1b3eff1214bf2b9d862b2aacc1f04c9ee9e44f47252e81b81c9f276c
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    linux/amd64

  Name:        docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0@sha256:7e695e85941c5cfda8abc924d8d4d44531a7841e96ce126ee852dd9cb8cbefdc
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    linux/arm64

  Name:        docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0@sha256:7d29cae98fb1ffe72050ffc35df7576dbd6d2b87b2898d7f7794455c48b5cb51
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    unknown/unknown
  Annotations:
    vnd.docker.reference.digest: sha256:85f9517c1b3eff1214bf2b9d862b2aacc1f04c9ee9e44f47252e81b81c9f276c
    vnd.docker.reference.type:   attestation-manifest

  Name:        docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0@sha256:80476d54a831524b1ba122f1041497f99be99cf2cb1f53bbed72f3148d9000f2
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    unknown/unknown
  Annotations:
    vnd.docker.reference.digest: sha256:7e695e85941c5cfda8abc924d8d4d44531a7841e96ce126ee852dd9cb8cbefdc
    vnd.docker.reference.type:   attestation-manifest
```
---

## Punkt 2 – Obraz multiplatformowy z wykorzystaniem cache (eksporter registry + backend inline)

### Pierwsze budowanie z eksportem cache do registry

Budowanie obrazu z jednoczesnym eksportem danych cache do osobnego taga `:cache` na DockerHub:
```angular2html
PS C:\Studia\chmura\chmura_zad1> docker buildx build --platform linux/amd64,linux/arm64 -t leprex24/pawcho-sawicki:weather-app.v.1.0 --cache-to type=registry,ref=leprex24/pawcho-sawicki:cache,mode=max --cache-from type=registry,ref=leprex24/pawcho-sawicki:cache --push .
[+] Building 72.9s (30/30) FINISHED                                                       docker-container:multibuilder
 => [internal] load build definition from Dockerfile                                                               0.1s
 => => transferring dockerfile: 788B                                                                               0.1s
 => resolve image config for docker-image://docker.io/docker/dockerfile:1                                          3.4s
 => [auth] docker/dockerfile:pull token for registry-1.docker.io                                                   0.0s
 => CACHED docker-image://docker.io/docker/dockerfile:1@sha256:2780b5c3bab67f1f76c781860de469442999ed1a0d7992a5ef  0.0s
 => => resolve docker.io/docker/dockerfile:1@sha256:2780b5c3bab67f1f76c781860de469442999ed1a0d7992a5efdf2cffc0e3d  0.0s
 => [linux/amd64 internal] load metadata for docker.io/library/python:3.12-alpine                                  1.2s
 => [linux/arm64 internal] load metadata for docker.io/library/python:3.12-alpine                                  1.2s
 => [auth] library/python:pull token for registry-1.docker.io                                                      0.0s
 => [internal] load .dockerignore                                                                                  0.1s
 => => transferring context: 84B                                                                                   0.0s
 => ERROR importing cache manifest from leprex24/pawcho-sawicki:cache                                              3.5s
 => [linux/amd64 builder 1/4] FROM docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcb  0.1s
 => => resolve docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcbd00adfca247b2c27051a  0.1s
 => [internal] load build context                                                                                  0.0s
 => => transferring context: 133B                                                                                  0.0s
 => [linux/arm64 builder 1/4] FROM docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcb  0.1s
 => => resolve docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcbd00adfca247b2c27051a  0.1s
 => [auth] leprex24/pawcho-sawicki:pull token for registry-1.docker.io                                             0.0s
 => CACHED [linux/amd64 builder 2/4] WORKDIR /app                                                                  0.0s
 => CACHED [linux/amd64 builder 3/4] COPY requirements.txt .                                                       0.0s
 => CACHED [linux/amd64 builder 4/4] RUN pip install --no-cache-dir --prefix=/install -r requirements.txt          0.0s
 => CACHED [linux/amd64 stage-1 3/6] COPY --from=builder /install /usr/local                                       0.0s
 => CACHED [linux/amd64 stage-1 4/6] COPY main.py .                                                                0.0s
 => CACHED [linux/amd64 stage-1 5/6] COPY templates/ templates/                                                    0.0s
 => CACHED [linux/amd64 stage-1 6/6] RUN adduser -D uzytkownik                                                     0.0s
 => CACHED [linux/arm64 builder 2/4] WORKDIR /app                                                                  0.0s
 => CACHED [linux/arm64 builder 3/4] COPY requirements.txt .                                                       0.0s
 => CACHED [linux/arm64 builder 4/4] RUN pip install --no-cache-dir --prefix=/install -r requirements.txt          0.0s
 => CACHED [linux/arm64 stage-1 3/6] COPY --from=builder /install /usr/local                                       0.0s
 => CACHED [linux/arm64 stage-1 4/6] COPY main.py .                                                                0.0s
 => CACHED [linux/arm64 stage-1 5/6] COPY templates/ templates/                                                    0.0s
 => CACHED [linux/arm64 stage-1 6/6] RUN adduser -D uzytkownik                                                     0.0s
 => exporting to image                                                                                             7.6s
 => => exporting layers                                                                                            0.0s
 => => exporting manifest sha256:85f9517c1b3eff1214bf2b9d862b2aacc1f04c9ee9e44f47252e81b81c9f276c                  0.0s
 => => exporting config sha256:77135b7de71d5c39b5766e25f4b68cb4b5851f6e36c524e0594941511517e319                    0.0s
 => => exporting attestation manifest sha256:5517e945f971cb3a82cdfa0ff3e29f79c988fc8de41a63ea0cd65dcd9cbe3a15      0.1s
 => => exporting manifest sha256:7e695e85941c5cfda8abc924d8d4d44531a7841e96ce126ee852dd9cb8cbefdc                  0.0s
 => => exporting config sha256:3b8538d0bf48845a252433123b1749ed382e86b3bdfb50551148d600c95a1138                    0.0s
 => => exporting attestation manifest sha256:a294f279d233132a0301a47cf0c698510a2747e87a81575f2f4d22c5028991e6      0.1s
 => => exporting manifest list sha256:b9d2c402ada38cecdf5689367a9ddc2acb6727f6d0e212dcb2d15de4b9c73166             0.0s
 => => pushing layers                                                                                              3.3s
 => => pushing manifest for docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0@sha256:b9d2c402ada38cecdf5689367a  4.1s
 => exporting cache to registry                                                                                   63.3s
 => => preparing build cache for export                                                                            4.4s
 => => sending cache export                                                                                       58.9s
 => => writing layer sha256:3124cc6c064bced8b2c441577d9c793d290258b2eb87477d21572e5a938fb3cb                       0.2s
 => => writing layer sha256:2374f5dabbbd61e8a675ebe34a8d78df784231817839246e8389166107af3ff3                       0.2s
 => => writing layer sha256:05b6ee55fad38c6a3dc2ee84c7a44ff2b3429fc3eef0d4c2a2cfeb230b0acd73                       0.2s
 => => writing layer sha256:254ac41e2afd13e7a1276627191463329b96d835eab35e7804fdad56d7e363d5                       0.2s
 => => writing layer sha256:34c2cfc552748cea5709f52df10cfbcf4b9980128e7fc7fadb204c12836d8716                      54.1s
 => => writing layer sha256:3a212b73b0f481530087068db8052331bc5e6e38a7f945ddf3f5a954084b04c7                       0.2s
 => => writing layer sha256:3a4f2e6e1560fccb75f8aa9c6b7458b3179164f6378b125e533286c88351cd2a                       0.1s
 => => writing layer sha256:5ad4ca0c526e79e9ee3aaa54e1adabd86676181fa909e412e4c407cc09e2f77f                       0.3s
 => => writing layer sha256:69f0330a42ae1900749a2318c25833e092dbbd921908d3285555d90742b33dd7                       1.5s
 => => writing layer sha256:6a0ac1617861a677b045b7ff88545213ec31c0ff08763195a70a4a5adda577bb                       0.1s
 => => writing layer sha256:737a5d42f5c1a5292ff120293ae321b7840e582c3d1e8c3060e16e2cf1a281e0                       0.8s
 => => writing layer sha256:74bec20749987ddac4cc74bd2f826b97908f1c8a71661be8e89e6e8468e634d9                       0.2s
 => => writing layer sha256:7f74e9681a48bb56c6270dfdcd8ccf43803ebeb715670dd77e49c63ef0d1fcdf                       0.2s
 => => writing layer sha256:ab2a8d22c2ee9acda4d837b784cc0148e4e77c399ef5bb15937f3d29bd5a8d34                       0.1s
 => => writing layer sha256:abfeb14e5b99ef23e1eac610aadc5c77dcca74a43ada6cdc13c226cbc9baa2f9                       0.2s
 => => writing layer sha256:b581ffef5567fe137dc88da5e25a79760e81d697c336e147aaba34fe6a15c1da                       0.2s
 => => writing layer sha256:c1b6dac650c3be39f73d649ca2d9ce4188602303a9b0c9192a6aca486671487c                       0.2s
 => => writing layer sha256:c302fa6e284f7ed4e781207e091f39b576e90557d9c0791d080e27b24e280a2f                       0.7s
 => => writing layer sha256:d13065f73e4adc05b1faa7dee6e2948f4087190967c6cbb8f0646a95d8cfdc48                      49.3s
 => => writing layer sha256:d17f077ada118cc762df373ff803592abf2dfa3ddafaa7381e364dd27a88fca7                       0.3s
 => => writing layer sha256:e2ec11d2fa78b536de278cc161362488d70db1afa0b34bce52a9dcca7266ff31                       1.4s
 => => writing layer sha256:fd21a26fb55d22baaa317c98a4296e6a284dd39cc0f9e68ef781bb74adfd6dc7                       0.1s
 => => writing config sha256:12734aaf01e2c260fbc7c137ebba3143dbf4ce65b001ea8d8b2425ec42dc0091                      1.3s
 => => writing cache image manifest sha256:11d6ef0ffece7f778c00fbfc35a076e268703fa6897c4af0b38770074581e07d        3.4s
 => [auth] leprex24/pawcho-sawicki:pull,push token for registry-1.docker.io                                        0.0s
------
 > importing cache manifest from leprex24/pawcho-sawicki:cache:
------

View build details: docker-desktop://dashboard/build/multibuilder/multibuilder0/px097gdkoe4wi1sxpadaa8rz8
```

### Drugie budowanie – weryfikacja że cache jest wykorzystywany
```angular2html
PS C:\Studia\chmura\chmura_zad1> docker buildx build --platform linux/amd64,linux/arm64 -t leprex24/pawcho-sawicki:weather-app.v.1.0 --cache-to type=registry,ref=leprex24/pawcho-sawicki:cache,mode=max --cache-from type=registry,ref=leprex24/pawcho-sawicki:cache --push .
[+] Building 20.1s (27/27) FINISHED                                                       docker-container:multibuilder
 => [internal] load build definition from Dockerfile                                                               0.0s
 => => transferring dockerfile: 788B                                                                               0.0s
 => resolve image config for docker-image://docker.io/docker/dockerfile:1                                          2.5s
 => CACHED docker-image://docker.io/docker/dockerfile:1@sha256:2780b5c3bab67f1f76c781860de469442999ed1a0d7992a5ef  0.0s
 => => resolve docker.io/docker/dockerfile:1@sha256:2780b5c3bab67f1f76c781860de469442999ed1a0d7992a5efdf2cffc0e3d  0.0s
 => [linux/amd64 internal] load metadata for docker.io/library/python:3.12-alpine                                  0.8s
 => [linux/arm64 internal] load metadata for docker.io/library/python:3.12-alpine                                  0.3s
 => [internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 84B                                                                                   0.0s
 => importing cache manifest from leprex24/pawcho-sawicki:cache                                                    7.4s
 => => inferred cache manifest type: application/vnd.oci.image.manifest.v1+json                                    0.0s
 => [internal] load build context                                                                                  0.0s
 => => transferring context: 133B                                                                                  0.0s
 => [linux/amd64 builder 1/4] FROM docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcb  0.1s
 => => resolve docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcbd00adfca247b2c27051a  0.0s
 => [linux/arm64 builder 1/4] FROM docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcb  0.0s
 => => resolve docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcbd00adfca247b2c27051a  0.0s
 => CACHED [linux/arm64 builder 2/4] WORKDIR /app                                                                  0.0s
 => CACHED [linux/arm64 stage-1 6/6] RUN adduser -D uzytkownik                                                     0.6s
 => CACHED [linux/arm64 stage-1 5/6] COPY templates/ templates/                                                    0.0s
 => CACHED [linux/arm64 stage-1 4/6] COPY main.py .                                                                0.0s
 => CACHED [linux/arm64 stage-1 3/6] COPY --from=builder /install /usr/local                                       0.0s
 => CACHED [linux/arm64 builder 4/4] RUN pip install --no-cache-dir --prefix=/install -r requirements.txt          0.0s
 => CACHED [linux/arm64 builder 3/4] COPY requirements.txt .                                                       0.0s
 => CACHED [linux/amd64 stage-1 3/6] COPY --from=builder /install /usr/local                                       0.0s
 => CACHED [linux/amd64 stage-1 6/6] RUN adduser -D uzytkownik                                                     0.6s
 => CACHED [linux/amd64 stage-1 5/6] COPY templates/ templates/                                                    0.0s
 => CACHED [linux/amd64 stage-1 4/6] COPY main.py .                                                                0.0s
 => CACHED [linux/amd64 builder 2/4] WORKDIR /app                                                                  0.0s
 => CACHED [linux/amd64 builder 4/4] RUN pip install --no-cache-dir --prefix=/install -r requirements.txt          0.0s
 => CACHED [linux/amd64 builder 3/4] COPY requirements.txt .                                                       0.0s
 => exporting to image                                                                                             7.7s
 => => exporting layers                                                                                            0.0s
 => => exporting manifest sha256:85f9517c1b3eff1214bf2b9d862b2aacc1f04c9ee9e44f47252e81b81c9f276c                  0.0s
 => => exporting config sha256:77135b7de71d5c39b5766e25f4b68cb4b5851f6e36c524e0594941511517e319                    0.0s
 => => exporting attestation manifest sha256:7d29cae98fb1ffe72050ffc35df7576dbd6d2b87b2898d7f7794455c48b5cb51      0.0s
 => => exporting manifest sha256:7e695e85941c5cfda8abc924d8d4d44531a7841e96ce126ee852dd9cb8cbefdc                  0.0s
 => => exporting config sha256:3b8538d0bf48845a252433123b1749ed382e86b3bdfb50551148d600c95a1138                    0.0s
 => => exporting attestation manifest sha256:80476d54a831524b1ba122f1041497f99be99cf2cb1f53bbed72f3148d9000f2      0.0s
 => => exporting manifest list sha256:ab2d5f34eaf591c0db9c04c3e42190bb742727517d975621398b6c1dd276d6c3             0.0s
 => => pushing layers                                                                                              2.6s
 => => pushing manifest for docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0@sha256:ab2d5f34eaf591c0db9c04c3e4  4.9s
 => exporting cache to registry                                                                                    7.4s
 => => preparing build cache for export                                                                            0.8s
 => => sending cache export                                                                                        6.6s
 => => writing layer sha256:05b6ee55fad38c6a3dc2ee84c7a44ff2b3429fc3eef0d4c2a2cfeb230b0acd73                       1.2s
 => => writing layer sha256:254ac41e2afd13e7a1276627191463329b96d835eab35e7804fdad56d7e363d5                       1.2s
 => => writing layer sha256:2374f5dabbbd61e8a675ebe34a8d78df784231817839246e8389166107af3ff3                       1.3s
 => => writing layer sha256:3124cc6c064bced8b2c441577d9c793d290258b2eb87477d21572e5a938fb3cb                       1.2s
 => => writing layer sha256:34c2cfc552748cea5709f52df10cfbcf4b9980128e7fc7fadb204c12836d8716                       0.2s
 => => writing layer sha256:3a212b73b0f481530087068db8052331bc5e6e38a7f945ddf3f5a954084b04c7                       0.2s
 => => writing layer sha256:3a4f2e6e1560fccb75f8aa9c6b7458b3179164f6378b125e533286c88351cd2a                       0.3s
 => => writing layer sha256:5ad4ca0c526e79e9ee3aaa54e1adabd86676181fa909e412e4c407cc09e2f77f                       0.1s
 => => writing layer sha256:69f0330a42ae1900749a2318c25833e092dbbd921908d3285555d90742b33dd7                       0.2s
 => => writing layer sha256:6a0ac1617861a677b045b7ff88545213ec31c0ff08763195a70a4a5adda577bb                       0.2s
 => => writing layer sha256:737a5d42f5c1a5292ff120293ae321b7840e582c3d1e8c3060e16e2cf1a281e0                       0.2s
 => => writing layer sha256:74bec20749987ddac4cc74bd2f826b97908f1c8a71661be8e89e6e8468e634d9                       0.2s
 => => writing layer sha256:7f74e9681a48bb56c6270dfdcd8ccf43803ebeb715670dd77e49c63ef0d1fcdf                       0.2s
 => => writing layer sha256:ab2a8d22c2ee9acda4d837b784cc0148e4e77c399ef5bb15937f3d29bd5a8d34                       0.2s
 => => writing layer sha256:abfeb14e5b99ef23e1eac610aadc5c77dcca74a43ada6cdc13c226cbc9baa2f9                       0.1s
 => => writing layer sha256:b581ffef5567fe137dc88da5e25a79760e81d697c336e147aaba34fe6a15c1da                       0.1s
 => => writing layer sha256:c1b6dac650c3be39f73d649ca2d9ce4188602303a9b0c9192a6aca486671487c                       0.1s
 => => writing layer sha256:c302fa6e284f7ed4e781207e091f39b576e90557d9c0791d080e27b24e280a2f                       0.2s
 => => writing layer sha256:d13065f73e4adc05b1faa7dee6e2948f4087190967c6cbb8f0646a95d8cfdc48                       0.1s
 => => writing layer sha256:d17f077ada118cc762df373ff803592abf2dfa3ddafaa7381e364dd27a88fca7                       0.2s
 => => writing layer sha256:e2ec11d2fa78b536de278cc161362488d70db1afa0b34bce52a9dcca7266ff31                       0.1s
 => => writing layer sha256:fd21a26fb55d22baaa317c98a4296e6a284dd39cc0f9e68ef781bb74adfd6dc7                       0.1s
 => => writing config sha256:2812aed75761f28397b623c5d3d653cdf4466f9edea7b846c50178a89c9db935                      0.1s
 => => writing cache image manifest sha256:7ac7a48e2516b448b74c0e58d2788fb49cda88c998f478726795adf42f8b1ade        4.5s
 => [auth] leprex24/pawcho-sawicki:pull,push token for registry-1.docker.io                                        0.0s

View build details: docker-desktop://dashboard/build/multibuilder/multibuilder0/vjafjyaq73nvc89vhrwvq16fk
```
Widać że cache działa `importing cache manifest from leprex24/pawcho-sawicki:cache` i czas wykonania polecenia skrócił się z 72 sekund do 20.

### Weryfikacja że obraz cache istnieje w registry
```angular2html
PS C:\Studia\chmura\chmura_zad1> docker buildx imagetools inspect leprex24/pawcho-sawicki:cache
Name:      docker.io/leprex24/pawcho-sawicki:cache
MediaType: application/vnd.oci.image.manifest.v1+json
Digest:    sha256:7ac7a48e2516b448b74c0e58d2788fb49cda88c998f478726795adf42f8b1ade
```
---

## Punkt 3 – Obraz multiplatformowy z kodem pobieranym z GitHub przez mount secret + cache w trybie max

Punkt 3 zawiera wszystko z punktów 1 i 2 oraz dodatkowo kod aplikacji pobierany jest bezpośrednio z publicznego repozytorium GitHub podczas budowania obrazu z wykorzystaniem funkcjonalności `mount secret` rozszerzonego frontendu buildkit.

### Repozytorium GitHub

Kod aplikacji dostępny jest pod adresem:
https://github.com/Leprex24/weather-app

### Dockerfile z rozszerzonym frontendem buildkit i mount secret
```dockerfile
# syntax=docker/dockerfile:1.4
FROM python:3.12-alpine AS builder
WORKDIR /app

# Instalacja git potrzebnego do pobrania kodu z GitHub
RUN apk add --no-cache git

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Pobieranie kodu z publicznego repozytorium GitHub przez mount secret
RUN --mount=type=secret,id=github_token \
    TOKEN=$(cat /run/secrets/github_token 2>/dev/null || echo "") && \
    if [ -n "$TOKEN" ]; then \
        git clone https://$TOKEN@github.com/leprex24/weather-app.git /src; \
    else \
        git clone https://github.com/leprex24/weather-app.git /src; \
    fi

FROM python:3.12-alpine

LABEL org.opencontainers.image.authors="Kacper Sawicki" \
      org.opencontainers.image.title="Aplikacja pogodowa zad1" \
      org.opencontainers.image.version="1.0.0"

WORKDIR /app

COPY --from=builder /install /usr/local

# Kopiowanie kodu pobranego z GitHub w etapie builder
COPY --from=builder /src/main.py .
COPY --from=builder /src/templates/ templates/

RUN adduser -D uzytkownik
USER uzytkownik

ENV PORT=8080
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD wget -qO- http://127.0.0.1:8080/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "main:app"]
```
### Budowanie obrazu z cache w trybie max i mount secret

Dla publicznego repozytorium GitHub (bez tokena):
```angular2html
PS C:\Studia\chmura\chmura_zad1> docker buildx imagetools inspect leprex24/pawcho-sawicki:cache
Name:      docker.io/leprex24/pawcho-sawicki:cache
MediaType: application/vnd.oci.image.manifest.v1+json
Digest:    sha256:7ac7a48e2516b448b74c0e58d2788fb49cda88c998f478726795adf42f8b1ade
PS C:\Studia\chmura\chmura_zad1> docker buildx build --platform linux/amd64,linux/arm64 -t leprex24/pawcho-sawicki:weather-app.v.1.0 --cache-to type=registry,ref=leprex24/pawcho-sawicki:cache,mode=max --cache-from type=registry,ref=leprex24/pawcho-sawicki:cache --push .
[+] Building 179.4s (34/34) FINISHED                                                      docker-container:multibuilder
 => [internal] load build definition from Dockerfile                                                               0.1s
 => => transferring dockerfile: 1.38kB                                                                             0.0s
 => resolve image config for docker-image://docker.io/docker/dockerfile:1.4                                        2.6s
 => [auth] docker/dockerfile:pull token for registry-1.docker.io                                                   0.0s
 => docker-image://docker.io/docker/dockerfile:1.4@sha256:9ba7531bd80fb0a858632727cf7a112fbfd19b17e94c4e84ced81e  10.4s
 => => resolve docker.io/docker/dockerfile:1.4@sha256:9ba7531bd80fb0a858632727cf7a112fbfd19b17e94c4e84ced81e24ef1  0.0s
 => => sha256:1328b32c40fca9bcf9d70d8eccb72eb873d1124d72dadce04db8badbe7b08546 9.94MB / 9.94MB                     9.9s
 => => extracting sha256:1328b32c40fca9bcf9d70d8eccb72eb873d1124d72dadce04db8badbe7b08546                          0.4s
 => [internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 84B                                                                                   0.0s
 => [linux/arm64 internal] load metadata for docker.io/library/python:3.12-alpine                                  0.6s
 => [linux/amd64 internal] load metadata for docker.io/library/python:3.12-alpine                                  0.6s
 => [auth] library/python:pull token for registry-1.docker.io                                                      0.0s
 => importing cache manifest from leprex24/pawcho-sawicki:cache                                                    3.1s
 => => inferred cache manifest type: application/vnd.oci.image.manifest.v1+json                                    0.0s
 => [linux/amd64 builder 1/6] FROM docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcb  0.1s
 => => resolve docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcbd00adfca247b2c27051a  0.1s
 => [linux/arm64 builder 1/6] FROM docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcb  0.1s
 => => resolve docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcbd00adfca247b2c27051a  0.1s
 => [internal] load build context                                                                                  0.1s
 => => transferring context: 37B                                                                                   0.0s
 => [auth] leprex24/pawcho-sawicki:pull token for registry-1.docker.io                                             0.0s
 => CACHED [linux/arm64 builder 2/6] WORKDIR /app                                                                  0.1s
 => CACHED [linux/amd64 builder 2/6] WORKDIR /app                                                                  0.1s
 => [linux/amd64 builder 3/6] RUN apk add --no-cache git                                                           6.9s
 => [linux/arm64 builder 3/6] RUN apk add --no-cache git                                                           8.9s
 => [linux/amd64 builder 4/6] COPY requirements.txt .                                                              0.1s
 => [linux/amd64 builder 5/6] RUN pip install --no-cache-dir --prefix=/install -r requirements.txt                 9.8s
 => [linux/arm64 builder 4/6] COPY requirements.txt .                                                              0.1s
 => [linux/arm64 builder 5/6] RUN pip install --no-cache-dir --prefix=/install -r requirements.txt                54.0s
 => [linux/amd64 builder 6/6] RUN --mount=type=secret,id=github_token     TOKEN=$(cat /run/secrets/github_token 2  2.7s
 => [linux/amd64 stage-1 3/6] COPY --from=builder /install /usr/local                                              0.3s
 => [linux/amd64 stage-1 4/6] COPY --from=builder /src/main.py .                                                   0.1s
 => [linux/amd64 stage-1 5/6] COPY --from=builder /src/templates/ templates/                                       0.1s
 => [linux/amd64 stage-1 6/6] RUN adduser -D uzytkownik                                                            0.2s
 => [linux/arm64 builder 6/6] RUN --mount=type=secret,id=github_token     TOKEN=$(cat /run/secrets/github_token 2  3.9s
 => [linux/arm64 stage-1 3/6] COPY --from=builder /install /usr/local                                              0.2s
 => [linux/arm64 stage-1 4/6] COPY --from=builder /src/main.py .                                                   0.1s
 => [linux/arm64 stage-1 5/6] COPY --from=builder /src/templates/ templates/                                       0.1s
 => [linux/arm64 stage-1 6/6] RUN adduser -D uzytkownik                                                            0.3s
 => exporting to image                                                                                            57.6s
 => => exporting layers                                                                                            1.1s
 => => exporting manifest sha256:66a8f71d6ef02f124b21e35e1bf4e3167be17bd85681a0bbcc45fab6358689d6                  0.0s
 => => exporting config sha256:a38f205eebfb2cf61c9fd9d0261659cac50ff72f74ce692bace2e808186c429c                    0.0s
 => => exporting attestation manifest sha256:be19d3bc6d37f66d39bf2f42f7672b5cce83477b1c7679bdce05af76c239c8af      0.0s
 => => exporting manifest sha256:33b046b60d8d87ed402a811db431c60e067439a987ab8bc245dad8fe6a292a93                  0.0s
 => => exporting config sha256:b3bea3ec5c360125ff1088d57e7a94a61319d777185649299c0cbea9dc9bd1a0                    0.0s
 => => exporting attestation manifest sha256:76bb1f436bb610ffa5ff6eba5cdab72693726e259a029a17dba5e45c6c7489a8      0.1s
 => => exporting manifest list sha256:f5a26cc2b6bfba6a67c06fa4494d4c079be2977d0cf83f0e47fca5b9fb1825e2             0.0s
 => => pushing layers                                                                                             49.5s
 => => pushing manifest for docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0@sha256:f5a26cc2b6bfba6a67c06fa449  7.2s
 => exporting cache to registry                                                                                   92.0s
 => => preparing build cache for export                                                                            2.0s
 => => sending cache export                                                                                       90.0s
 => => writing layer sha256:21981f47ab91795aada711bf518f736efa6b5d6a5b67bc758c6641eca14f85b1                      47.7s
 => => writing layer sha256:0c35f75a2524a366aec8fc67ef54e0406e7567dbb7558e6f0ba013e3bfec004a                      39.6s
 => => writing layer sha256:05b6ee55fad38c6a3dc2ee84c7a44ff2b3429fc3eef0d4c2a2cfeb230b0acd73                       0.4s
 => => writing layer sha256:1e858d171d7c0d6f55041df51633ffaca77d0e827480ac21c88e1416e2e4fe71                      26.8s
 => => writing layer sha256:235a35bc26a9a8a308fd1363e32fa34a212bd49f6344a8e0d8829eaa665b3781                      27.3s
 => => writing layer sha256:254ac41e2afd13e7a1276627191463329b96d835eab35e7804fdad56d7e363d5                       0.3s
 => => writing layer sha256:26995c766b46dc1efcd82e3e46196d915986d4c0daf447e270a2ead33c82e82a                       2.2s
 => => writing layer sha256:3124cc6c064bced8b2c441577d9c793d290258b2eb87477d21572e5a938fb3cb                       0.3s
 => => writing layer sha256:3a4f2e6e1560fccb75f8aa9c6b7458b3179164f6378b125e533286c88351cd2a                       0.3s
 => => writing layer sha256:3ec1764723d1a0b914efbe3b956796bbf03dfa1afd687edcf318c4a77034f6c1                       0.5s
 => => writing layer sha256:4b5c8c0be95df6f9dc52712a5a3579f649f07229d79128839297f44d77ab21e1                       0.3s
 => => writing layer sha256:6a0ac1617861a677b045b7ff88545213ec31c0ff08763195a70a4a5adda577bb                       0.5s
 => => writing layer sha256:737a5d42f5c1a5292ff120293ae321b7840e582c3d1e8c3060e16e2cf1a281e0                       0.6s
 => => writing layer sha256:74bec20749987ddac4cc74bd2f826b97908f1c8a71661be8e89e6e8468e634d9                       0.8s
 => => writing layer sha256:90d2c33ac51ce86074e6e107142241727a1b716c46a514c58195038b6b3e1ea5                      12.8s
 => => writing layer sha256:959750cc8d7beeca6338bc0cdbac0f092e0b6bd94f89cec088e2467e039836c2                      53.8s
 => => writing layer sha256:abfeb14e5b99ef23e1eac610aadc5c77dcca74a43ada6cdc13c226cbc9baa2f9                       1.7s
 => => writing layer sha256:d12be2017ae6cd160ce8cb13e0fd6443ff5c66c74d111d86ba67c38c4d044dcf                      26.1s
 => => writing layer sha256:d17f077ada118cc762df373ff803592abf2dfa3ddafaa7381e364dd27a88fca7                       0.6s
 => => writing layer sha256:d388060985c53cfc92290f9a488825b85769212f97aaa658af581bae835d2c61                      43.1s
 => => writing layer sha256:daec1c6d352e1d763a410aec27f8af705586ae27eb73abcdcb114cea43e56764                       1.8s
 => => writing layer sha256:e50ff5035762aab8d00a5b22502898d9fd8ef629a8b7e01c9a5a04daa25589b6                       0.5s
 => => writing layer sha256:e6f07cc9800f2f74a9738168755963d7ea8bf6c0d1726b9dfa41b24e606211e8                       0.2s
 => => writing layer sha256:f11220fc6faf7f82799b3a1569b0a67f4d9bb413850413092792ed90fd68e929                       0.5s
 => => writing layer sha256:f961240cb284c35f8705f87362b3014bad7c537f492c88711149245d7c9e6688                       0.5s
 => => writing layer sha256:fd21a26fb55d22baaa317c98a4296e6a284dd39cc0f9e68ef781bb74adfd6dc7                       0.3s
 => => writing config sha256:fd58a3ef5fb6fc9f6770e4c6a349b35c73fcd8ecfe1f055e48cfdbffe541ac11                      1.2s
 => => writing cache image manifest sha256:d34a9659be9794799bc703a98fe0d94247b6e5b581397e78ce979fc77bacbf7e        2.3s
 => [auth] leprex24/pawcho-sawicki:pull,push token for registry-1.docker.io                                        0.0s

View build details: docker-desktop://dashboard/build/multibuilder/multibuilder0/ltynudojxlnq2ukfe21rjqjrd
```
### Drugie budowanie – weryfikacja cache
Wynik (fragment z widocznym CACHED i skróconym czasem wykonania potwierdzający wykorzystanie cache):
```angular2html
PS C:\Studia\chmura\chmura_zad1> docker buildx build --platform linux/amd64,linux/arm64 -t leprex24/pawcho-sawicki:weather-app.v.1.0 --cache-to type=registry,ref=leprex24/pawcho-sawicki:cache,mode=max --cache-from type=registry,ref=leprex24/pawcho-sawicki:cache --push .
[+] Building 11.7s (31/31) FINISHED                                                       docker-container:multibuilder
 => [internal] load build definition from Dockerfile                                                               0.0s
 => => transferring dockerfile: 1.38kB                                                                             0.0s
 => resolve image config for docker-image://docker.io/docker/dockerfile:1.4                                        1.6s
 => CACHED docker-image://docker.io/docker/dockerfile:1.4@sha256:9ba7531bd80fb0a858632727cf7a112fbfd19b17e94c4e84  0.0s
 => => resolve docker.io/docker/dockerfile:1.4@sha256:9ba7531bd80fb0a858632727cf7a112fbfd19b17e94c4e84ced81e24ef1  0.0s
 => [internal] load .dockerignore                                                                                  0.1s
 => => transferring context: 84B                                                                                   0.0s
 => [linux/amd64 internal] load metadata for docker.io/library/python:3.12-alpine                                  0.4s
 => [linux/arm64 internal] load metadata for docker.io/library/python:3.12-alpine                                  0.7s
 => importing cache manifest from leprex24/pawcho-sawicki:cache                                                    2.1s
 => => inferred cache manifest type: application/vnd.oci.image.manifest.v1+json                                    0.0s
 => [internal] load build context                                                                                  0.0s
 => => transferring context: 37B                                                                                   0.0s
 => [linux/arm64 builder 1/6] FROM docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcb  0.0s
 => => resolve docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcbd00adfca247b2c27051a  0.0s
 => [linux/amd64 builder 1/6] FROM docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcb  0.1s
 => => resolve docker.io/library/python:3.12-alpine@sha256:236173eb74001afe2f60862de935b74fcbd00adfca247b2c27051a  0.0s
 => CACHED [linux/amd64 builder 2/6] WORKDIR /app                                                                  0.0s
 => CACHED [linux/amd64 builder 3/6] RUN apk add --no-cache git                                                    0.0s
 => CACHED [linux/amd64 builder 4/6] COPY requirements.txt .                                                       0.0s
 => CACHED [linux/amd64 builder 5/6] RUN pip install --no-cache-dir --prefix=/install -r requirements.txt          0.0s
 => CACHED [linux/amd64 builder 6/6] RUN --mount=type=secret,id=github_token     TOKEN=$(cat /run/secrets/github_  0.0s
 => CACHED [linux/amd64 stage-1 3/6] COPY --from=builder /install /usr/local                                       0.0s
 => CACHED [linux/amd64 stage-1 4/6] COPY --from=builder /src/main.py .                                            0.0s
 => CACHED [linux/amd64 stage-1 5/6] COPY --from=builder /src/templates/ templates/                                0.0s
 => CACHED [linux/amd64 stage-1 6/6] RUN adduser -D uzytkownik                                                     0.6s
 => CACHED [linux/arm64 builder 2/6] WORKDIR /app                                                                  0.0s
 => CACHED [linux/arm64 builder 3/6] RUN apk add --no-cache git                                                    0.0s
 => CACHED [linux/arm64 builder 4/6] COPY requirements.txt .                                                       0.0s
 => CACHED [linux/arm64 builder 5/6] RUN pip install --no-cache-dir --prefix=/install -r requirements.txt          0.0s
 => CACHED [linux/arm64 builder 6/6] RUN --mount=type=secret,id=github_token     TOKEN=$(cat /run/secrets/github_  0.0s
 => CACHED [linux/arm64 stage-1 3/6] COPY --from=builder /install /usr/local                                       0.0s
 => CACHED [linux/arm64 stage-1 4/6] COPY --from=builder /src/main.py .                                            0.0s
 => CACHED [linux/arm64 stage-1 5/6] COPY --from=builder /src/templates/ templates/                                0.0s
 => CACHED [linux/arm64 stage-1 6/6] RUN adduser -D uzytkownik                                                     0.6s
 => exporting to image                                                                                             6.7s
 => => exporting layers                                                                                            0.0s
 => => exporting manifest sha256:66a8f71d6ef02f124b21e35e1bf4e3167be17bd85681a0bbcc45fab6358689d6                  0.0s
 => => exporting config sha256:a38f205eebfb2cf61c9fd9d0261659cac50ff72f74ce692bace2e808186c429c                    0.0s
 => => exporting attestation manifest sha256:152178b0af07ff2b1cde0c03e2ba615574d7a9f1175afd5b1284144aa830328d      0.0s
 => => exporting manifest sha256:33b046b60d8d87ed402a811db431c60e067439a987ab8bc245dad8fe6a292a93                  0.0s
 => => exporting config sha256:b3bea3ec5c360125ff1088d57e7a94a61319d777185649299c0cbea9dc9bd1a0                    0.0s
 => => exporting attestation manifest sha256:db44097f76b2d5801c5667d73c60e00b5ac9ae0e8cbbd5e662c5a9f3df4eea29      0.1s
 => => exporting manifest list sha256:e5adf30cfe2320d238e19dd2a3402a916b9556a3b7c28a1e14fe6a3c69b56e20             0.0s
 => => pushing layers                                                                                              2.9s
 => => pushing manifest for docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0@sha256:e5adf30cfe2320d238e19dd2a3  3.6s
 => exporting cache to registry                                                                                    2.8s
 => => preparing build cache for export                                                                            1.2s
 => => sending cache export                                                                                        1.6s
 => => writing layer sha256:21981f47ab91795aada711bf518f736efa6b5d6a5b67bc758c6641eca14f85b1                       0.2s
 => => writing layer sha256:0c35f75a2524a366aec8fc67ef54e0406e7567dbb7558e6f0ba013e3bfec004a                       0.3s
 => => writing layer sha256:05b6ee55fad38c6a3dc2ee84c7a44ff2b3429fc3eef0d4c2a2cfeb230b0acd73                       0.3s
 => => writing layer sha256:1e858d171d7c0d6f55041df51633ffaca77d0e827480ac21c88e1416e2e4fe71                       0.2s
 => => writing layer sha256:235a35bc26a9a8a308fd1363e32fa34a212bd49f6344a8e0d8829eaa665b3781                       0.2s
 => => writing layer sha256:254ac41e2afd13e7a1276627191463329b96d835eab35e7804fdad56d7e363d5                       0.2s
 => => writing layer sha256:26995c766b46dc1efcd82e3e46196d915986d4c0daf447e270a2ead33c82e82a                       0.2s
 => => writing layer sha256:3124cc6c064bced8b2c441577d9c793d290258b2eb87477d21572e5a938fb3cb                       0.2s
 => => writing layer sha256:3a4f2e6e1560fccb75f8aa9c6b7458b3179164f6378b125e533286c88351cd2a                       0.2s
 => => writing layer sha256:3ec1764723d1a0b914efbe3b956796bbf03dfa1afd687edcf318c4a77034f6c1                       0.2s
 => => writing layer sha256:4b5c8c0be95df6f9dc52712a5a3579f649f07229d79128839297f44d77ab21e1                       0.2s
 => => writing layer sha256:6a0ac1617861a677b045b7ff88545213ec31c0ff08763195a70a4a5adda577bb                       0.1s
 => => writing layer sha256:737a5d42f5c1a5292ff120293ae321b7840e582c3d1e8c3060e16e2cf1a281e0                       0.1s
 => => writing layer sha256:74bec20749987ddac4cc74bd2f826b97908f1c8a71661be8e89e6e8468e634d9                       0.2s
 => => writing layer sha256:90d2c33ac51ce86074e6e107142241727a1b716c46a514c58195038b6b3e1ea5                       0.2s
 => => writing layer sha256:959750cc8d7beeca6338bc0cdbac0f092e0b6bd94f89cec088e2467e039836c2                       0.2s
 => => writing layer sha256:abfeb14e5b99ef23e1eac610aadc5c77dcca74a43ada6cdc13c226cbc9baa2f9                       0.1s
 => => writing layer sha256:d12be2017ae6cd160ce8cb13e0fd6443ff5c66c74d111d86ba67c38c4d044dcf                       0.1s
 => => writing layer sha256:d17f077ada118cc762df373ff803592abf2dfa3ddafaa7381e364dd27a88fca7                       0.2s
 => => writing layer sha256:d388060985c53cfc92290f9a488825b85769212f97aaa658af581bae835d2c61                       0.1s
 => => writing layer sha256:daec1c6d352e1d763a410aec27f8af705586ae27eb73abcdcb114cea43e56764                       0.2s
 => => writing layer sha256:e50ff5035762aab8d00a5b22502898d9fd8ef629a8b7e01c9a5a04daa25589b6                       0.2s
 => => writing layer sha256:e6f07cc9800f2f74a9738168755963d7ea8bf6c0d1726b9dfa41b24e606211e8                       0.3s
 => => writing layer sha256:f11220fc6faf7f82799b3a1569b0a67f4d9bb413850413092792ed90fd68e929                       0.3s
 => => writing layer sha256:f961240cb284c35f8705f87362b3014bad7c537f492c88711149245d7c9e6688                       0.2s
 => => writing layer sha256:fd21a26fb55d22baaa317c98a4296e6a284dd39cc0f9e68ef781bb74adfd6dc7                       0.2s
 => => writing config sha256:fd58a3ef5fb6fc9f6770e4c6a349b35c73fcd8ecfe1f055e48cfdbffe541ac11                      0.2s
 => => writing cache image manifest sha256:d34a9659be9794799bc703a98fe0d94247b6e5b581397e78ce979fc77bacbf7e        0.2s
 => [auth] leprex24/pawcho-sawicki:pull,push token for registry-1.docker.io                                        0.0s

View build details: docker-desktop://dashboard/build/multibuilder/multibuilder0/za4vl1iiuzm90ba7ofufpt50k
```
### Weryfikacja manifestu – obie platformy
```angular2html
PS C:\Studia\chmura\chmura_zad1> docker buildx imagetools inspect leprex24/pawcho-sawicki:weather-app.v.1.0
Name:      docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0
MediaType: application/vnd.oci.image.index.v1+json
Digest:    sha256:e5adf30cfe2320d238e19dd2a3402a916b9556a3b7c28a1e14fe6a3c69b56e20

Manifests:
  Name:        docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0@sha256:66a8f71d6ef02f124b21e35e1bf4e3167be17bd85681a0bbcc45fab6358689d6
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    linux/amd64

  Name:        docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0@sha256:33b046b60d8d87ed402a811db431c60e067439a987ab8bc245dad8fe6a292a93
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    linux/arm64

  Name:        docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0@sha256:152178b0af07ff2b1cde0c03e2ba615574d7a9f1175afd5b1284144aa830328d
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    unknown/unknown
  Annotations:
    vnd.docker.reference.digest: sha256:66a8f71d6ef02f124b21e35e1bf4e3167be17bd85681a0bbcc45fab6358689d6
    vnd.docker.reference.type:   attestation-manifest

  Name:        docker.io/leprex24/pawcho-sawicki:weather-app.v.1.0@sha256:db44097f76b2d5801c5667d73c60e00b5ac9ae0e8cbbd5e662c5a9f3df4eea29
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    unknown/unknown
  Annotations:
    vnd.docker.reference.digest: sha256:33b046b60d8d87ed402a811db431c60e067439a987ab8bc245dad8fe6a292a93
    vnd.docker.reference.type:   attestation-manifest
```

### Weryfikacja obrazu cache w registry
```angular2html
PS C:\Studia\chmura\chmura_zad1> docker buildx imagetools inspect leprex24/pawcho-sawicki:cache
Name:      docker.io/leprex24/pawcho-sawicki:cache
MediaType: application/vnd.oci.image.manifest.v1+json
Digest:    sha256:d34a9659be9794799bc703a98fe0d94247b6e5b581397e78ce979fc77bacbf7e
```
---

## Linki

- Repozytorium GitHub: https://github.com/Leprex24/weather-app
- Repozytorium DockerHub: https://hub.docker.com/repository/docker/leprex24/pawcho-sawicki/general
