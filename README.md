Design Logic and Trade-offs

Flink: 
1. Validate  event 
2. update aggregated rolling 
3. Join streaming acticity features with demographic features 
4. Apply scaling (same as training), for early standardization and consistent features downstream
5. send request to the scoring container in sagemaker 




(base) ➜  easy-go-takehome curl -X POST http://localhost:8000/score -H 'Content-Type: application/json' --data @test.json
{"fraud_flag":false,"fraud_probability":0.4042387390188852}
