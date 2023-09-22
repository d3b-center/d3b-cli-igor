import d3b_cli_igor.common
import boto3, numpy, sys, time, json

logger = d3b_cli_igor.common.get_logger(
    __name__, testing_mode=False, log_format="detailed"
)

#Set app cluster name
ecs_client = d3b_cli_igor.common.setup("ecs")
ecr_client = d3b_cli_igor.common.setup("ecr")

def list_ecr_images():
    logger.info("Getting images from ECR repos")
    repos = ecr_client.describe_repositories()
    container_images = []
    for r in repos['repositories']:
        images = ecr_client.list_images(
            repositoryName = r['repositoryName']
        )
        for i in images['imageIds']:
            if 'imageTag' in i:
                image_name = r['repositoryUri'] + ":" + i['imageTag']
                container_images.append({"image": image_name, "digest": i["imageDigest"]})
    return container_images

def list_running_task_images(app_cluster):
    logger.info("Getting images from RUNNING tasks, from " + app_cluster + "cluster")
    ecs_tasks = []
    images = []
    services = ecs_client.list_services(
        cluster=(app_cluster),
        maxResults=100,
        launchType="FARGATE"
    )
    for i in services["serviceArns"]:
        task = ecs_client.list_tasks(
            cluster=(app_cluster),
            maxResults=100,
            serviceName=i,
            desiredStatus='RUNNING',
            launchType='FARGATE'
        )
        ecs_tasks = ecs_tasks + task['taskArns']
    #Check for empty running tasks
    if len(ecs_tasks) > 0: 
        tasks_details = ecs_client.describe_tasks( cluster=app_cluster, tasks=ecs_tasks)
        for t in tasks_details['tasks']:
            for c in t['containers']:
                images.append({"image": c['image'], "digest": c['imageDigest']})
    return images

def list_active_task_definitions():
    logger.info("Getting images from Task Definitions")
    ecs_tasks = []
    images = []
    tds = ecs_client.list_task_definitions(
        status='ACTIVE'
    )
    for i in tds["taskDefinitionArns"]:
        td = ecs_client.describe_task_definition(taskDefinition=i)
        for c in td['taskDefinition']['containerDefinitions']:
            images.append({"image": c['image'], "digest": ""})
    #Since task definiteions do not have image digest, we need to look it up
    for i in list_ecr_images():
        for idx,ti in enumerate(images):
            if ( ti['image'] in i['image']):
                images[idx]['digest'] = i['digest']
    return images

def list_clusters():
    clusters = []
    for c in ecs_client.list_clusters()['clusterArns']:
        clusters.append(c.split('/')[1])
    return clusters

def get_list_of_old_images(active_images, ecr_images):
    images_to_remove = []
    digests_to_keep = []
    items_to_remove = []
    for i in ecr_images:
        found = False
        for ai in active_images:
            if( i["digest"] == ai['digest']):
                found = True
        if (found == False):
            items_to_remove.append(i)
        else:
            found = False

    logger.info("Items to remove before: " + str(len(items_to_remove)))

    #Since each image can have multiple tags, we need to go through images and find which ones have different tag but does not need to be removed
    for d in digests_to_keep:
        for idx,i in enumerate(items_to_remove):
            if( d["digest"] == i["digest"]):
                items_to_remove.pop(idx)

    logger.info("Images to remove : "+ str(len(items_to_remove)))

    return items_to_remove

def ecr_cleanup():
    ecs_images = []
    ecr_images = list_ecr_images()
    task_def_images = []

    for c in list_clusters():
        ecs_images = ecs_images + list_running_task_images(c)

    task_def_images = list_active_task_definitions()
    print(len(task_def_images))

    logger.info("Number of ECR images in all ECR repos: " + str(len(ecr_images)))
    logger.info("Number of images in task definitions: "+str(len(task_def_images)))
    logger.info("Number of images in running tasks: "+str(len(ecs_images)))

    #Find which images to remove
    active_images = (task_def_images + ecs_images)
    logger.info("Number of total active images: " + str(len(active_images)))
    get_list_of_old_images(active_images,ecr_images)
