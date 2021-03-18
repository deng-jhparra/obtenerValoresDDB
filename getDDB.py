import json
import boto3
from boto3.dynamodb.conditions import Key

def query_scan (dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('prod.RetailTraders')

    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan()
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None

    lista = []
    for user in range(len(response['Items'])):
        usuario = response['Items'][user]['userName']
        status = None
        try:
            status = response['Items'][user]['additionalInfo']['reviewStatus']
        except KeyError:
            status = None
        verificado = int(response['Items'][user]['verified'])
        creadoel = response['Items'][user]['createdAtUtc']
        try:
            modificadoel = response['Items'][user]['modifyAtUtc']
        except KeyError:
            modificadoel = None
        if len(response['Items'][user]['bankList']) > 0:
            for bank in range(len(response['Items'][user]['bankList'])):
                registro = {}
                registro["user"] = usuario
                registro["status"] = status
                registro["createdAtUtc"] = creadoel
                registro["modifyAtUtc"] = modificadoel
                registro["verified"] = verificado
                registro["bank"] = response['Items'][user]['bankList'][bank]['name']
                #print(registro)
                lista.append(registro)
        else :
            registro = {}
            registro["user"] = usuario
            registro["status"] = status
            registro["createdAtUtc"] = creadoel
            registro["modifyAtUtc"] = modificadoel
            registro["verified"] = verificado
            registro["bank"] = None
            #print(registro)
            lista.append(registro)
    #print(lista)
    jsonString = json.dumps(lista)
    print(jsonString)
   

if __name__ == '__main__':
    query_scan()
