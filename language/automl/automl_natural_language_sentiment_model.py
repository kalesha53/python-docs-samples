#!/usr/bin/env python

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations on model
with the Google AutoML Natural Language API.

For more information, see the tutorial page at
https://cloud.google.com/natural-language/automl/docs/
"""

import argparse
import os
from datetime import datetime    

def create_model(project_id, compute_region, dataset_id, model_name):
    """Create a sentiment model."""
    # [START automl_natural_language_create_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # dataset_id = '[DATASET_ID]'
    # model_name = '[MODEL_NAME]'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = client.location_path(project_id, compute_region)

    # Set model name and model metadata for the dataset.
    my_model = {
        "display_name": model_name,
        "dataset_id": dataset_id,
        "text_sentiment_model_metadata": {},
    }

    # Create a model with the model metadata in the region.
    response = client.create_model(project_location, my_model)
    print("Training operation name: {}".format(response.operation.name))
    print("Training started...")

    # [END automl_natural_language_create_model]


def get_operation_status(operation_full_id):
    """Get operation status."""
    # [START automl_natural_language_get_operation_status]
    # TODO(developer): Uncomment and set the following variables
    # operation_full_id =
    #   'projects/<projectId>/locations/<region>/operations/<operationId>'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the latest state of a long-running operation.
    response = client.transport._operations_client.get_operation(
        operation_full_id
    )

    print("Operation status: {}".format(response))

    # [END automl_natural_language_get_operation_status]


def list_models(project_id, compute_region, filter_):
    """List all models."""
    # [START automl_natural_language_list_models]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # filter_ = 'text_sentiment_model_metadata:*'

    from google.cloud import automl_v1beta1 as automl
    from google.cloud.automl_v1beta1 import enums

    client = automl.AutoMlClient()

    # A resource that represents Google Cloud Platform location.
    project_location = client.location_path(project_id, compute_region)

    # List all the models available in the region by applying filter.
    response = client.list_models(project_location, filter_)

    print("List of models:")
    for model in response:
        # Retrieve deployment state.
        deployment_state = ""
        if model.deployment_state == enums.Model.DeploymentState.DEPLOYED:
            deployment_state = "deployed"
        else:
            deployment_state = "undeployed"

        # Display the model information.
        print("Model name: {}".format(model.name))
        print("Model id: {}".format(model.name.split("/")[-1]))
        print("Model display name: {}".format(model.display_name))
        print("Model create time: {}".format(datetime.fromtimestamp(model.create_time.seconds).strftime("%Y-%m-%dT%H:%M:%SZ")))
        print("Model deployment state: {}".format(deployment_state))

    # [END automl_natural_language_list_models]


def get_model(project_id, compute_region, model_id):
    """Get model details."""
    # [START automl_natural_language_get_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # model_id = '[MODEL_ID]'

    from google.cloud import automl_v1beta1 as automl
    from google.cloud.automl_v1beta1 import enums

    client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = client.model_path(project_id, compute_region, model_id)

    # Get complete detail of the model.
    model = client.get_model(model_full_id)

    # Retrieve deployment state.
    deployment_state = ""
    if model.deployment_state == enums.Model.DeploymentState.DEPLOYED:
        deployment_state = "deployed"
    else:
        deployment_state = "undeployed"

    # Display the model information.
    print("Model name: {}".format(model.name))
    print("Model id: {}".format(model.name.split("/")[-1]))
    print("Model display name: {}".format(model.display_name))
    print("Model create time: {}".format(datetime.fromtimestamp(model.create_time.seconds).strftime("%Y-%m-%dT%H:%M:%SZ")))
    print("Model deployment state: {}".format(deployment_state))

    # [END automl_natural_language_get_model]


def list_model_evaluations(project_id, compute_region, model_id):
    """List model evaluations."""
    # [START automl_natural_language_list_model_evaluations]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # model_id = '[MODEL_ID]'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = client.model_path(project_id, compute_region, model_id)

    # List all the model evaluations in the model by applying filter.
    response = client.list_model_evaluations(model_full_id)

    print("List of model evaluations:")
    for element in response:
        print(element)

    # [END automl_natural_language_list_model_evaluations]


def get_model_evaluation(
    project_id, compute_region, model_id, model_evaluation_id
):
    """Get model evaluation."""
    # [START automl_natural_language_get_model_evaluation]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # model_id = '[MODEL_ID]'
    # model_evaluation_id = '[MODEL_EVALUATION_ID]'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the model evaluation.
    model_evaluation_full_id = client.model_evaluation_path(
        project_id, compute_region, model_id, model_evaluation_id
    )

    # Get complete detail of the model evaluation.
    response = client.get_model_evaluation(model_evaluation_full_id)

    print("Sentiment model precision: {}".format(response.text_sentiment_evaluation_metrics.precision))
    print("Sentiment model recall: {}".format(response.text_sentiment_evaluation_metrics.recall))
    print("Sentiment model f1 score: {}".format(response.text_sentiment_evaluation_metrics.f1_score))

    # [END automl_natural_language_get_model_evaluation]
    
    
def display_evaluation(project_id, compute_region, model_id):
    """Display evaluation."""
    # [START automl_natural_language_display_evaluation]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # model_id = '[MODEL_ID]'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = client.model_path(project_id, compute_region, model_id)

    # List all the model evaluations in the model by applying filter.
    response = client.list_model_evaluations(model_full_id)

    # Iterate through the results.
    for element in response:
        # There is evaluation for each class in a model and for overall model.
        # Get only the evaluation of overall model.
        if not element.annotation_spec_id:
            model_evaluation_id = element.name.split("/")[-1]

    # Resource name for the model evaluation.
    model_evaluation_full_id = client.model_evaluation_path(
        project_id, compute_region, model_id, model_evaluation_id
    )

    # Get a model evaluation.
    model_evaluation = client.get_model_evaluation(model_evaluation_full_id)

    sentiment_metrics = model_evaluation.text_sentiment_evaluation_metrics

    print(
        "Model Precision: {}%".format(
            round(sentiment_metrics.precision * 100, 2)
        )
    )
    print(
        "Model Recall: {}%".format(
            round(sentiment_metrics.recall * 100, 2)
        )
    )
    print(
        "Model F1 score: {}%".format(
            round(sentiment_metrics.f1_score * 100, 2)
        )
    )
    print(
        "Model absolute error: {}%".format(
            round(sentiment_metrics.mean_absolute_error * 100, 2)
        )
    )
    print(
        "Model mean squared error: {}%".format(
            round(sentiment_metrics.mean_squared_error * 100, 2)
        )
    )
    print(
        "Model linear kappa: {}%".format(
            round(sentiment_metrics.linear_kappa * 100, 2)
        )
    )
    print(
        "Model quadratic kappa: {}%".format(
            round(sentiment_metrics.quadratic_kappa * 100, 2)
        )
    )

    # [END automl_natural_language_display_evaluation]


def delete_model(project_id, compute_region, model_id):
    """Delete a model."""
    # [START automl_natural_language_delete_model]
    # TODO(developer): Uncomment and set the following variables
    # project_id = '[PROJECT_ID]'
    # compute_region = '[COMPUTE_REGION]'
    # model_id = '[MODEL_ID]'

    from google.cloud import automl_v1beta1 as automl

    client = automl.AutoMlClient()

    # Get the full path of the model.
    model_full_id = client.model_path(project_id, compute_region, model_id)

    # Delete a model.
    response = client.delete_model(model_full_id)

    # synchronous check of operation status.
    print("Model deleted. {}".format(response.result()))

    # [END automl_natural_language_delete_model]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    create_model_parser = subparsers.add_parser(
        "create_model", help=create_model.__doc__
    )
    create_model_parser.add_argument("dataset_id")
    create_model_parser.add_argument("model_name")

    get_operation_status_parser = subparsers.add_parser(
        "get_operation_status", help=get_operation_status.__doc__
    )
    get_operation_status_parser.add_argument("operation_full_id")

    list_models_parser = subparsers.add_parser(
        "list_models", help=list_models.__doc__
    )
    list_models_parser.add_argument(
        "filter_", nargs="?", default="text_sentiment_model_metadata:*")

    get_model_parser = subparsers.add_parser(
        "get_model", help=get_model_evaluation.__doc__
    )
    get_model_parser.add_argument("model_id")

    list_model_evaluations_parser = subparsers.add_parser(
        "list_model_evaluations", help=list_model_evaluations.__doc__
    )
    list_model_evaluations_parser.add_argument("model_id")

    get_model_evaluation_parser = subparsers.add_parser(
        "get_model_evaluation", help=get_model_evaluation.__doc__
    )
    get_model_evaluation_parser.add_argument("model_id")
    get_model_evaluation_parser.add_argument("model_evaluation_id")

    display_evaluation_parser = subparsers.add_parser(
        "display_evaluation", help=display_evaluation.__doc__
    )
    display_evaluation_parser.add_argument("model_id")

    delete_model_parser = subparsers.add_parser(
        "delete_model", help=delete_model.__doc__
    )
    delete_model_parser.add_argument("model_id")

    project_id = os.environ["PROJECT_ID"]
    compute_region = os.environ["REGION_NAME"]

    args = parser.parse_args()

    if args.command == "create_model":
        create_model(
            project_id, compute_region, args.dataset_id, args.model_name
        )
    if args.command == "get_operation_status":
        get_operation_status(args.operation_full_id)
    if args.command == "list_models":
        list_models(project_id, compute_region, args.filter_)
    if args.command == "get_model":
        get_model(project_id, compute_region, args.model_id)
    if args.command == "list_model_evaluations":
        list_model_evaluations(
            project_id, compute_region, args.model_id
        )
    if args.command == "get_model_evaluation":
        get_model_evaluation(
            project_id, compute_region, args.model_id, args.model_evaluation_id
        )
    if args.command == "display_evaluation":
        display_evaluation(
            project_id, compute_region, args.model_id
        )
    if args.command == "delete_model":
        delete_model(project_id, compute_region, args.model_id)
