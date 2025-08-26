pip install --force-reinstall --no-cache-dir --extra-index-url http://devpiread:Devpiread123@10.12.0.78:13141/root/dev/+simple/ --trusted-host 10.12.0.78  pyspl==0.1.0

python ecdh_ke_test_grcp.py 0 JG0100021700000000 10000
python ecdh_ke_test_grcp.py 1 JG0100021600000000 10000


python psi_test_grpc.py 0 JG0100021700000000 1 2 10000
python psi_test_grpc.py 1 JG0100021600000000 1 2 10000

python circuit_psi_test_grpc.py 0 JG0100020500000000 
python circuit_psi_test_grpc.py 1 JG0100020600000000 