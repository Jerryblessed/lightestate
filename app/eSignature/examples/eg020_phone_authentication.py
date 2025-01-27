import base64
from os import path
from flask import current_app as app, session, request
from docusign_esign import AccountsApi, EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Tabs, Recipients
from docusign_esign.client.api_exception import ApiException
from ...consts import pattern
from ...docusign import create_api_client
from ...error_handlers import process_error


class Eg020PhoneAuthenticationController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        country_code = pattern.sub("", request.form.get("country_code"))
        phone_number = pattern.sub("", request.form.get("phone_number"))
        document = request.files.get("document")

        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "phone_number": phone_number,
            "country_code": country_code,
            "document": document,
            "status": "sent",
            "workflow_id": session['workflow_id']
        }
        args = {
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
            "envelope_args": envelope_args
        }
        return args

    @staticmethod
    def worker(args):
        """1. Create an API client 2. Create an envelope definition object"""
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        envelope_definition = EnvelopeDefinition(email_subject="Please sign this document set")

        # Process uploaded document
        uploaded_file = args["envelope_args"]["document"]
        content_bytes = uploaded_file.read()
        base64_file_content = base64.b64encode(content_bytes).decode("ascii")

        # Add a document
        document1 = Document(
            document_base64=base64_file_content,
            document_id="1",
            file_extension="pdf",
            name=uploaded_file.filename
        )

        envelope_definition.documents = [document1]
        envelope_definition.status = args["envelope_args"]["status"]

        # Create your signature tab
        sign_here1 = SignHere(
            name="SignHereTab",
            anchor_string="/sn1/",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20",
            tab_label="SignHereTab",
            page_number="1",
            document_id="1",
            recipient_id="1"
        )

        signer1 = Signer(
            email=args["envelope_args"]["signer_email"],
            name=args["envelope_args"]["signer_name"],
            recipient_id="1",
            routing_order="1",
            identity_verification={
                "workflowId": session['workflow_id'],
                "steps": "null",
                "inputOptions": [
                    {"name": "phone_number_list", "valueType": "PhoneNumberList",
                     "phoneNumberList": [{"countryCode": args["envelope_args"]["country_code"], 
                                          "code": "1", 
                                          "number": args["envelope_args"]["phone_number"]}]}
                ],
                "idCheckConfigurationName": ""
            },
            tabs=Tabs(sign_here_tabs=[sign_here1])
        )

        envelope_definition.recipients = Recipients(signers=[signer1])

        # Call the eSignature REST API
        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)
        return results


    @staticmethod
    def get_workflow(args):
        """Retrieve the workflow id"""
        try:
            api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
            #ds-snippet-start:eSign20Step3
            workflow_details = AccountsApi(api_client)
            workflow_response = workflow_details.get_account_identity_verification(account_id=args["account_id"])

            # Check that idv authentication is enabled
            # Find the workflow ID corresponding to the name "Phone Authentication"
            if workflow_response.identity_verification:
                for workflow in workflow_response.identity_verification:
                    if workflow.default_name == "Phone Authentication":
                        session['workflow_id'] = workflow.workflow_id
            #ds-snippet-end:eSign20Step3
                return session['workflow_id']

            else:
                return None

        except ApiException as err:
            return process_error(err)
    
