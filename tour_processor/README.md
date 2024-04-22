# Testing

- Create a Personal Access Token for GitLab and login to docker with it:
```shell
docker login registry.gitlab.com -u YourGitlabUsername
```
- Pull the docker image with this command:

```shell
docker pull registry.gitlab.com/zino.studio/tour/tour_processor:main
```

- Prepare your image directory
- Run the program with this command:

```shell
docker run -v "$(pwd)/images:/tmp/images" registry.gitlab.com/zino.studio/tour/tour_processor:main python3 run.py /tmp/images --output /tmp/images/output.jpg
```

You will see the output in the `output.jpg` file located in the images folder.\
For having a good result go to 'https://renderstuff.com/tools/360-panorama-web-viewer/' and see!