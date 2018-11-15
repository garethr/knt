
# KNT

`knt` is a simple utility for working with [Knative Build](https://github.com/knative/build). Specifically it helps with understanding and installing the various `BuildTemplates` currently available.

The tool maintains a list of known BuildTemplates (this is in lieu of a proper index or discovery mechanism) and makes referencing those templates by short name easy. For other templates you'll need to provide a full URL to the resource definition. You can list known templates with `knt list`:


```console
$ knt list
----------  ----------------------------------------------------------------------------------------------
buildah     https://raw.githubusercontent.com/knative/build-templates/master/buildah/buildah.yaml
kaniko      https://raw.githubusercontent.com/knative/build-templates/master/kaniko/kaniko.yaml
buildpack   https://raw.githubusercontent.com/knative/build-templates/master/buildpack/buildpack.yaml
bazel       https://raw.githubusercontent.com/knative/build-templates/master/bazel/bazel.yaml
jib-maven   https://raw.githubusercontent.com/knative/build-templates/master/jib/jib-maven.yaml
jib-gradle  https://raw.githubusercontent.com/knative/build-templates/master/jib/jib-gradle.yaml
buildkit    https://raw.githubusercontent.com/knative/build-templates/master/buildkit/1-buildtemplate.yaml
----------  ----------------------------------------------------------------------------------------------
```


You're now probably wondering what the user interface for those templates is. `knt inspect` will produce a human readable summary:

```console
$ knt inspect buildah
buildah
https://raw.githubusercontent.com/knative/build-templates/master/buildah/buildah.yaml

Parameters (4)    Description                                                                    Default
----------------  -----------------------------------------------------------------------------  ------------
BUILDER_IMAGE     The location of the buildah builder image.
IMAGE             The name of the image to push.
DOCKERFILE        Path to the Dockerfile to build.                                               ./Dockerfile
TLSVERIFY         Verify the TLS on the registry endpoint (for push/pull to a non-TLS registry)  true

Steps (2)    Image             Command    Args
-----------  ----------------  ---------  -------------------------
build        ${BUILDER_IMAGE}             bud
                                          --tls-verify=${TLSVERIFY}
                                          --layers
                                          -f
                                          ${DOCKERFILE}
                                          -t
                                          ${IMAGE}
                                          .
push         ${BUILDER_IMAGE}             push
                                          --tls-verify=${TLSVERIFY}
                                          ${IMAGE}
                                          docker://${IMAGE}
```

If you're now happy to install that template look no further than `knt install`:

```console
$ knt install kaniko
buildtemplate.build.knative.dev "kaniko" configured
```


## Docker

`knt` is also available as a Docker Image. Note that `install` will require you to mount your Kubernetes credentials and to for the container to have network access to the Kubernetes cluster.

```console
$ docker run --rm garethr/knt list
----------  ----------------------------------------------------------------------------------------------
buildah     https://raw.githubusercontent.com/knative/build-templates/master/buildah/buildah.yaml
kaniko      https://raw.githubusercontent.com/knative/build-templates/master/kaniko/kaniko.yaml
buildpack   https://raw.githubusercontent.com/knative/build-templates/master/buildpack/buildpack.yaml
bazel       https://raw.githubusercontent.com/knative/build-templates/master/bazel/bazel.yaml
jib-maven   https://raw.githubusercontent.com/knative/build-templates/master/jib/jib-maven.yaml
jib-gradle  https://raw.githubusercontent.com/knative/build-templates/master/jib/jib-gradle.yaml
buildkit    https://raw.githubusercontent.com/knative/build-templates/master/buildkit/1-buildtemplate.yaml
----------  ----------------------------------------------------------------------------------------------
```


## Usage

```console
Usage: command.py [OPTIONS] COMMAND [ARGS]...

  knt provides a number of tools for working with Knative Build Templates.

Options:
  --help  Show this message and exit.

Commands:
  inspect  Inspect a BuildTemplate by name or URL.
  install  Install a BuildTempate based on short name or URL.
  list     List known BuildTemplates.
  show     Show YAML document for named BuildTemplate.
```
