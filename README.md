# Overview

![Commit Activity](https://img.shields.io/github/commit-activity/m/tokujun-t/Stayforge)
![Codecov](https://codecov.io/gh/tokujun-t/Stayforge/branch/main/graph/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/tokujunsystem/stayforge.svg)
![PyPI Version](https://img.shields.io/pypi/v/stayforge)
![PyPI Downloads](https://img.shields.io/pypi/dm/stayforge)
![GitHub Workflow Status](https://github.com/tokujun-t/Stayforge/actions/workflows/docker-build-push.yml/badge.svg)
![GitHub Workflow Status](https://github.com/tokujun-t/Stayforge/actions/workflows/python-sdk.yml/badge.svg)

Stayforge is both an engine and a platform that simplifies the development and deployment of all stay-related
applications. Originally implemented in our company’s unmanned hotel project, Stayforge has evolved to support a wide
range of use cases. Beyond hotels, it can be applied to rental offices, parking lots, co-working spaces, serviced
apartments, smart retail centers, and even logistics hubs.

This versatile solution streamlines operational workflows by automating many of the tasks typically associated with
property management and service deployment. Whether you’re running a modern hospitality operation, managing urban rental
spaces, or overseeing any stay-centric business, Stayforge offers a comprehensive toolkit to accelerate innovation and
enhance efficiency.

https://www.stayforge.io

**Let’s take our time to read the document**

If you are too anxious and start reading from the middle of the document, you will most likely not be able to understand
the meaning. Therefore, we recommend that you read the documentation from scratch.

Or, you just want to quickly build a Stayforge for evaluation, we recommend using the Stayforge SaaS service (that is
free to a certain extent), or following the Quick Start chapter in the documentation to load your own server
environment.

## Quick Start

First, You need to deploy Stayforge first using Docker Compose or Kubernetes. The specific deployment instructions and
procedures are explained in detail in the Depoly chapter of the Stayforge document.

Second, after you deploy Stayforge, you have two options to operate Stayforge.

- Use the Stayforge API to operate Stayforge, which is mainly aimed at developer users.
- If you are not a developer, you can use Stayforge Foundry, which provides friendly graphics pages to help you run your
  business with Stayforge.

## Quick Start - Depoly Stayforge

Our Stayforge SaaS service provides a free one-click deployment service to a certain extent. On that day, we welcome you
to deploy it on your own server.

The specific detailed documentation is here:

You can deploy Stayforge through Docker or Kubernetes.Stayforge is Docker-based,
and you can also deploy with Google Cloud Run, etc. to save time.

## Quick Start - Use Stayforge API

All operations in Stayforge are done by the Web API.
The Stayforge API supported JWT to verify identity.

### Authenticate

Before you start, you need to get `access_token` & `refresh_token` to get access.

`access_token` is used to access the API, and the default is `60 * 60 * 24` seconds (24 hours). and,
`refresh_token`, used to refresh the API. The default is `60 * 60 * 24 * 30` seconds (30 days).

About the detailed API instructions, please refer to
details [Authentication](#/Authentication/authenticate_api_auth_authenticate_post)

## Tips

### Healthcheck

Healthcheck at `/api/healthcheck`. curl to check if the service is working.

```shell
curl -I https://<your service>/api/healthcheck
```

### Some Links

GitHub Repo
[https://github.com/tokujun-t/Stayforge](https://github.com/tokujun-t/Stayforge)

Wiki
[https://github.com/tokujun-t/Stayforge/wiki](https://github.com/tokujun-t/Stayforge/wiki)
