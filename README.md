# Portainer2Git
[Portainer](https://www.portainer.io/) is an Amazing tool to manage Docker deployments. It supports basic docker-compose as well as distributed Swarm environments.

Unfortunately, Portainer lacks support for versioning of docker-compose files and configurations. Moreover, it persists these files in conventional docker volumes, making it harder to get them back and store them for the long term.

**Portainer2Git** resolves this problem. It uses Portainer API in order to get docker-compose files and store them in a secure encrypted way (via [ansible-vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html)) in a configured [Git](https://git-scm.com/) repository.

## History
Core features of Portainer2Git have been created (as a challenge) in **one day**. The idea was to "break the case" while looking at "what we are capable of".

This challenge have been completed on 3rd May 2020.

## How it works
The workflow of Portainer2Git is this one :

1. The App is [configured and deployed](#general-configuration)
2. One or multiple Portainer instances are [added](#adding-portainers-and-stacks)
3. One or multiple stacks are [added](#adding-portainers-and-stacks) to the previously created Portainer instances
4. Portainer2Git automaticaly checks for changes in the configured stacks and save them to the configured git repository.

### How does Portainer2Git connect to the repository ?
Portainer2Git must be configured **with an SSH Key** that have read and write rights on the target repository.

### What is the structure used in the target repository ?
Portainer2Git will create its own files tree in the target git repository.

For instance, if we consider a Portainer2Git with two Portainer instances configured (respectively named `prod` and `preprod`) and one `app` stack for each of the portainer instances, the following file tree will be created :

```
.
|prod
|----> app.txt
|preprod
|----> app.txt
```

## Current limitations
As a *one day build* Portainer2Git actually (as of 5th May 2020) suffers from some limitations (that will eventually be removed in the future) :

* Only docker-compose (stacks) can be added. **Portainer Configs** will be added in a near future
* The persistance of Portainer2Git only supports mongodb at this time (MySQL will eventually be added)
* No frontend have been developped yet. Adding portainer instances and stacks (docker-compose) must be done via HTTP requests
* Test coverture is not yet optimal
* It is currently not possible to list added portainer instances and stacks

As Portainer2Git is a tool that we use, these limitations will surely be adressed in the future. Moreover, **do not hesitate to create issues or request new features.** MR are also welcomed when an issue or feature requests is accepted by the developping team.

## Running the app
It is **highly** advised to run this application as a Docker container.

Following this advice, this deployment guide will configure and launch the app via a `docker-compose.yml` synthax.

### General configuration
Here is an example configuration that **adapted to your needs and your configuration** should work for everyone.

```
version: "3"

services:
  mongo:
    image: mongo
    ports:
      - 27017:27017

  app:
    image: lauevrar77/portainer2git
    ports:
      - 5000:5000
    environment:
      mongo: mongo
      # mongo_username: mongo
      # mongo_password: mongo
      NEXT_CHECK_INTERVAL: 30
      PORTAINER_VALIDITY_TIMEOUT: 120
      GIT_USERNAME: ops
      GIT_EMAIL: ops@compagny.com
      VAULT_PASSWORD: random
      REMOTE_REPOSITORY: git@github.com:lauevrar77/changeme.git
      REPOSITORY_BRANCH: master
      LOCAL_REPOSITORY: resources/portainers
      SSH_KEY: >
        -----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQB+o27KH5sngeCgIAIbOcJNl2zfz/BEC6Uwjkxln4yuugdrty8B\nVnv75YGR5Yidw1PNKYNJYLts2N0+w+Lnq5V8BZiJvD9tJ8S3//06/non3uWl1nfA\nOPObWYPWbF/5TASFAY6YyL0QGoTVGZjm7K5Y9wNY3Xe2w+zqeypJwBOE1AWvQV01\n/3g7/+4m8o6I3GDVax1fepu0mDuUtNiw03eI4TCxoRIB3x4UmkjyAoN12DBSTfmL\nj7nNQ3kambmfIjkp9UKDPTpsQ593IpB+d2TmKBwU73QbuJoNKLOUaeFhYx0R5qwN\ndyiSVgTkNQd03X72xCOH4N2lwXwAB3rGbK2nAgMBAAECggEAHPkjVdcZVlaen8Py\n92ulir8ER8h5Pfg0GQHVdMKmGyuwmvJULMguoZkGpeyP7xhLSfsfcGBTQTn0lHGY\nrkxRbQiSt6B8Gmso1Lgapa6nIAwdGm4RA8eD5Jz8TsiIxK6hshSDHW1/4/lNPrwW\ngW7RDMWm3GP/Ca+VuqfnKuxpCtBshEz+Cz5uAtOxntgdJj7RltEceNyXUvFYXbd6\nPRtM7iSpynaM/qeQRswNDCy0mBBZ4HE+x+M/Ih+jZHlDgOb2CH/oZUJ1X5kdzwsT\nHXCCGsOswBsCFXHRhSSuJ2uaumeUtcZVcJ+tWrWo7XWRRhlx665XojXLWiBmWJQ7\n/Sej0QKBgQDIt4m7WIMkH9MRRktKS3hqF9sNQFTuIxZZKPdYvw6e5dmJe3Q/fpZ2\nLaV+NO0Q/Ml2D0nMSNFHv6cfesePsa5MRVg4mw/M+lpJzEm5MPGiiqAO+7zhpIea\nkRSusL3APKpGDniATnpFRE2QOXgTP8P0/BxPtVZPlen2qFe+450s2wKBgQChhKZ8\nD3gBLgFImiT2NTIcrxtK2t6DMy6T3VmWIUZ3s/lHRgNyBuky+gnufJWWc198efCO\nOAV0LlgzcjB6aL/rrEWba+bnNlEMlw+TcagM8m5HSeUxGtNQ+iU9vgvoxEBiaZSQ\nxUk08ZRuMa22PH9UsMqIUGH2LWrbaQ6v4G02JQKBgQC7KJlffhtateokM33FGzZ/\nBxuU8aXAICuYm+B4ej7x37XGwr0U777xF4M3ebaMnopkccEIoeWzl3wImH44+R9j\ns02eCsjjA5bpNXqRGphWThkNn6LybG6drCay9c8Zz/eeN6QZUBQnPpdsoonauRzJ\n9cOYd6ixsUJmY3beYnOO/QKBgGY9HVUyRXgZst5OFE905L+bZ98+I9NQto8KcgbC\nEWT8GzKucsfe8AZAl8DKQ7X0WeDlHwwnEey02UfXZDBX1gRMC9ORvZtlmnApvsZK\nD2ICoyOk9trabCC59pDal5dDgq3Ivy3Uc757nMUT1S2hpcfqEImwuBGoNhekrJNP\nsFGxAoGAGgrYS/wXJYutqD+Pnx7sep5IaBZNZ6l7LtjldUiIEWNSYFNDtgrHDogd\nPfDH60co9gZ0Yb+skV/LcDIbhprbvYFQn9Pk2rxLCr9gVfl5rjWuFdMR37HXtOgy\n9SdLWWvFmhx22sZxgnXukkaRqHP7hVLQci/9Z32P3q1pqGNaZjE=\n-----END RSA PRIVATE KEY-----\n
```
**IMPORTANT : AS IT IS PUBLIC NEVER USE THIS EXAMPLE PRIVATE KEY TO ACCESS YOUR GIT REPOSITORIES. CHANGE IT WITH ONE OF YOURS**

Here is a quick tour of the available configuration variables :

* `mongo`: Mongodb host
* `mongo_username`: Username to connect to mongodb. **Must be absent** if no authentication is requires
* `mongo_password`: Password to connect to mongodb. **Must be absent** if no authentication is requires
* `NEXT_CHECK_INTERVAL`: Delay (in seconds) between two executions of portainer instances checking. Default to 30.
* `PORTAINER_VALIDITY_TIMEOUT`: Delay (in seconds) before a portainer instance need to be saved again. Default to 120
* `GIT_USERNAME`: Username of Git user (as needed by `git config`). Default to ops
* `GIT_EMAIL`: Email of Git user (as needed by `git config`). Default to ops@compagny.com
* `VAULT_PASSWORD`: Encryption password for stack files. Mandatory with no default
* `REMOTE_REPOSITORY`: Remote Git repository cloning URL. It is advised to use an empty (containing just a readme file) repository. Mandatory with no default.
* `REPOSITORY_BRANCH`: Which is the branch to use on the repository (this parameter **have not been tested yet**). Default to master
* `LOCAL_REPOSITORY`: Repository path in the container. Can but should not be changed. Default to `resources/portainers`
* `SSH_KEY`: SSH private key to use when connecting to the repository. Not mandatory. See [SSH Configuration](#ssh-configuration)

It **must be noted** that the MongoDB database is **not** configurable and will be `portainer2git`. If you use authentication, please ensure that the configured user have access to this database.

### SSH configuration
As shown in the previous `docker-compose` example, the SSH key can be added directly in the environment of the running container.

However, it is possible to mount your key as a volume into the container.
The key should be mounted in the `/root/.ssh/id_rsa` file and have the correct rights for SSH the accept the key.

## Adding portainers and stacks
Currently adding portainer instances and stacks can only be done via HTTP requests.

### Adding a portainer instance
Request :
```
curl --request POST \
  --url http://localhost:5000/portainer \
  --header 'content-type: application/json' \
  --data '{
	"name": "prod",
	"endpoint": "http://portainer.compagny.com",
	"username": "admin",
	"password": "RandomPassword"
}'
```

Response :
```
{
  "portainer_id": "Portainer-bc88d39c-97b3-4f2e-88e3-aba652136ed8"
}
```

Due to the [current limitations](#current-limitations), it is important to **keep track** of the returned Portainer Id as it is **mandatory** to add stack to it.

### Adding a stack
Request :
```
curl --request POST \
  --url http://localhost:5000/portainer/stack/create \
  --header 'content-type: application/json' \
  --data '{
	"portainer_id": "Portainer-bc88d39c-97b3-4f2e-88e3-aba652136ed8",
	"stack_name": "app"
}'
```

There is no response to this request

## Future features

1. Allow to list portainer instances with their stacks + enhance test coverture
2. Allow to remove a stack in a portainer instance
3. Allow to remove a portainer instance
4. Allow to add and remove Portainer Configurations in portainer instance + save them to Git

## Contributing
Every feature request or issue is welcome. They must be done via the issues of this repository.

Once accepted by the maintainers, they will eventually be developped by the maintainers.
If you want to develop one of the **accepted features** yourself, feel free to make a Merge Request. Help is always welcome.

**Please note that each Merge Request should be made to the `dev` branch.**
