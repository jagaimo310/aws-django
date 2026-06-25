from django.shortcuts import render,redirect
import os
import boto3
import json
from . import forms
from . import models
from django.http import HttpResponse
# Create your views here.

def main(request):
    form = forms.prompt_form()
    return render(request,'main.html',context={'form':form})

def image(request):
    prompt = models.Prompt.objects.all()
    context_data = {'prompts':prompt}
    return render(request,'image.html',context = context_data)

def past(request):
    prompt = models.Prompt.objects.all()
    context_data = {'prompts':prompt}
    return render(request,'past.html',context = context_data)

# フォーム処理　プロンプト作成、ラムダ処理用
def prompt(request):
    form = forms.prompt_form(request.POST)
    # フォームのバリデーション
    if form.is_valid():
        prompt = form.cleaned_data['prompt']

    return lamda_invoke(request,prompt)
    
    # ラムダ呼び出し処理
def lamda_invoke(request,prompt):
    # AWSキー　IAMに置き換えるべし
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_DEFAULT_REGION")

    client = boto3.client(
        "lambda",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    # 呼び出し処理
    payload = {"body": json.dumps({"prompt": prompt})}
    response = client.invoke(
        FunctionName='arn:aws:lambda:us-west-2:905418432959:function:lab-bedrock-image-generator',
        InvocationType='RequestResponse',
        LogType='None',
        Payload=json.dumps(payload),
    )
    # 呼び出し結果を格納
    lambda_result = json.loads(response["Payload"].read())
    body_data = json.loads(lambda_result["body"])
    image_url = body_data.get("image_url")
    return data_set(request,prompt,image_url)

# データベース保存処理
def data_set(request,prompt,image_url):
    models.Prompt.objects.create(prompt=prompt ,image_url=image_url)

    # 値を入れてmainに返す
    form = forms.prompt_form(initial={"prompt": prompt})
    context_data = {'image_url':image_url,'form':form}
    return render(request,'main.html',context = context_data)

# プロンプト再利用
def prompt_recall(request,prompt_id):
    prompt = models.Prompt.objects.get(id = prompt_id)
    return lamda_invoke(request,prompt)
