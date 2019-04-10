Here's a quick idea for a stateless PaaS on top of Github and docker swarm.

You mark Github repos that you want to deploy to your Docker swarm with a certain tag, say "my-server".
Each repo has a docker-compose.yml file defining the stack needed to run it.
You have a daemon that periodically queries Github API for repos with given tag name (and from a certain user, for security reason). For every found repo it would do docker stack deploy RepoName --compose-file "...". Stacks would be deployed according to given service's deploy policy, utilizing its healthchecks etc.
So if you need to add a new repo to the swarm, you just mark it with a tag and wait a few min. If you need to update a service, you just edit its docker-compose.yml file and wait a few min. Secrets would be managed via docker secrets.

Advantages over plain swarm cluster?

Stateless. You don't have to remeber which stacks you need to deploy to which swarm in case of a crash. Also the state of the stacks deployed to swarm will never get out of sync with docker-compose.yml files defined in the repo.
People who want to deploy new stacks to the swarm don't need to have access to the swarm itself, only to managing Github repos. No need to bring some complicated management tools like Rancher.
