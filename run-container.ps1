$local_volume = $HOME + "/developments/image-recognition-trial"
$attached_volume = "/usr/src/project"
$volume = $local_volume + ":" + $attached_volume
$container = "kaggle/python"
docker run --rm -v $volume -it $container