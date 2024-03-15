"""
Utils to manage deployment of XGBoost classifier in CML
"""

class ModelDeployment():
    """
    Class to manage the model deployment of the xgboost model
    """

    def __init__(self, client, projectId, username, experimentName, experimentId):
        self.client = client
        self.projectId = projectId
        self.username = username
        self.experimentName = experimentName
        self.experimentId = experimentId

    def registerModelFromExperimentRun(self, modelName, experimentId, experimentRunId, modelPath, sessionId):
        """
        Method to register a model from an Experiment Run
        This is an alternative to the mlflow method to register a model via the register_model parameter in the log_model method
        Input: requires an experiment run
        Output:
        """

        model_name = 'wine_model_' + username + "-" + sessionId

        CreateRegisteredModelRequest = {
                                        "project_id": os.environ['CDSW_PROJECT_ID'],
                                        "experiment_id" : experimentId,
                                        "run_id": experimentRunId,
                                        "model_name": modelName,
                                        "model_path": modelPath
                                       }

        try:
            # Register a model.
            api_response = self.client.create_registered_model(CreateRegisteredModelRequest)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling CMLServiceApi->create_registered_model: %s\n" % e)

        return api_response

    def createPRDProject(self):
        """
        Method to create a PRD Project
        """

        createProjRequest = {"name": "MLOps Banking PRD", "template":"git", "git_url":"https://github.com/pdefusco/CML_MLOps_Banking_Demo_PRD.git"}

        try:
            # Create a new project
            api_response = self.client.create_project(createProjRequest)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling CMLServiceApi->create_project: %s\n" % e)

        return api_response

    def validatePRDProject(self, username):
        """
        Method to test successful project creation
        """

        try:
            # Return all projects, optionally filtered, sorted, and paginated.
            search_filter = {"owner.username" : username}
            search = json.dumps(search_filter)
            api_response = self.client.list_projects(search_filter=search)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling CMLServiceApi->list_projects: %s\n" % e)

        return api_response

    def createModel(self, projectId, modelName, modelId, description = "My Spark Clf"):
        """
        Method to create a model
        """

        CreateModelRequest = {
                                "project_id": projectId,
                                "name" : modelName,
                                "description": description,
                                "registered_model_id": modelId
                             }

        try:
            # Create a model.
            api_response = self.client.create_model(CreateModelRequest, projectId)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling CMLServiceApi->create_model: %s\n" % e)

        return api_response

    def createModelBuild(self, projectId, modelVersionId, modelCreationId):
        """
        Method to create a Model build
        """

        # Create Model Build
        CreateModelBuildRequest = {
                                    "registered_model_version_id": modelVersionId,
                                    "runtime_identifier": "docker.repository.cloudera.com/cloudera/cdsw/ml-runtime-workbench-python3.9-standard:2023.08.2-b8",
                                    "comment": "invoking model build",
                                    "model_id": modelCreationId
                                  }

        try:
            # Create a model build.
            api_response = self.client.create_model_build(CreateModelBuildRequest, projectId, modelCreationId)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling CMLServiceApi->create_model_build: %s\n" % e)

        return api_response

    def createModelDeployment(self, modelBuildId, projectId, modelCreationId):
        """
        Method to deploy a model build
        """

        CreateModelDeploymentRequest = {
          "cpu" : "2",
          "memory" : "4"
        }

        try:
            # Create a model deployment.
            api_response = self.client.create_model_deployment(CreateModelDeploymentRequest, projectId, modelCreationId, modelBuildId)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling CMLServiceApi->create_model_deployment: %s\n" % e)

        return api_response
