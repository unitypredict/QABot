
from unitypredict_engines import UnityPredictLocalHost
from unitypredict_engines import ChainedInferenceRequest, ChainedInferenceResponse, FileReceivedObj, FileTransmissionObj, IPlatform, InferenceRequest, InferenceResponse, OutcomeValue
import EntryPoint

if __name__ == "__main__":

    
    platform = UnityPredictLocalHost()

    testRequest = InferenceRequest()
    # User defined Input Values
    testRequest.InputValues = {
        "InputMessage": "What questions can you help me with?"
    } 

    results: InferenceResponse = EntryPoint.run_engine(testRequest, platform)

    # Print Outputs
    if (results.Outcomes != None):
        for outcomKeys, outcomeValues in results.Outcomes.items():
            print ("\n\nOutcome Key: {}".format(outcomKeys))
            for values in outcomeValues:
                infVal: OutcomeValue = values
                print ("Outcome Value: \n{}\n\n".format(infVal.Value))
                print ("Outcome Probability: \n{}\n\n".format(infVal.Probability))
    
    # Print Error Messages (if any)
    print ("Error Messages: {}".format(results.ErrorMessages))

        