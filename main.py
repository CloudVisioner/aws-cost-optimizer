import boto3
from tabulate import tabulate
import csv

def get_stopped_instances():
    ec2 = boto3.client('ec2')
    stopped = []

    res = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    for r in res['Reservations']:
        for i in r['Instances']:
            stopped.append({
                "Instance ID": i["InstanceId"],
                "Type": i["InstanceType"],
                "Region": ec2.meta.region_name
            })
    return stopped

def get_unattached_ebs():
    ec2 = boto3.client('ec2')
    volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    unused = []

    for v in volumes['Volumes']:
        cost = v['Size'] * 0.10  # example cost: $0.10/GB/month
        unused.append({
            "Volume ID": v['VolumeId'],
            "Size (GB)": v['Size'],
            "Monthly Cost Estimate ($)": round(cost, 2),
            "Region": ec2.meta.region_name
        })
    return unused

def save_to_csv(filename, data):
    if not data:
        print(f"[!] No data found for {filename}")
        return
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"[+] Saved: {filename}")

def main():
    print("\n[+] Getting stopped EC2 instances...")
    stopped_instances = get_stopped_instances()
    print(tabulate(stopped_instances, headers="keys"))

    print("\n[+] Getting unattached EBS volumes...")
    unused_volumes = get_unattached_ebs()
    print(tabulate(unused_volumes, headers="keys"))

    save_to_csv("stopped_instances.csv", stopped_instances)
    save_to_csv("unused_ebs_volumes.csv", unused_volumes)

def main():
    print("\n[+] Getting stopped EC2 instances...")
    stopped_instances = get_stopped_instances()
    for instance in stopped_instances:
        print(instance)

    print("\n[+] Getting unattached EBS volumes...")
    unused_volumes = get_unattached_ebs()
    for volume in unused_volumes:
        print(volume)

    # NEW CODE for RDS begins here
    print("\n[+] Getting RDS database instances...")
    rds_instances = get_rds_instances()
    for db in rds_instances:
        print(db)

    # Save all to CSV
    save_to_csv("stopped_instances.csv", stopped_instances)
    save_to_csv("unused_ebs_volumes.csv", unused_volumes)
    save_to_csv("rds_instances.csv", rds_instances)

def get_rds_instances():
    rds = boto3.client('rds')
    dbs = []

    try:
        response = rds.describe_db_instances()
        for db in response['DBInstances']:
            dbs.append({
                "DB Identifier": db.get("DBInstanceIdentifier", "N/A"),
                "Engine": db.get("Engine", "N/A"),
                "Status": db.get("DBInstanceStatus", "N/A"),
                "Region": rds.meta.region_name
            })
    except Exception as e:
        print("[!] Error getting RDS instances:", e)
    return dbs

def main():
    # Get instances
    stopped_instances = get_stopped_instances()
    unused_volumes = get_unattached_ebs()
    rds_instances = get_rds_instances()

    # Save CSVs
    save_to_csv("stopped_instances.csv", stopped_instances)
    save_to_csv("unused_ebs_volumes.csv", unused_volumes)
    save_to_csv("rds_instances.csv", rds_instances)

    # Total Cost Summary (MUST BE HERE inside main())
    total_cost = 0
    for volume in unused_volumes:
        total_cost += volume.get("Monthly Cost Estimate ($)", 0)

    print(f"\n[+] Estimated total monthly waste: ${total_cost:.2f}")

# This line stays outside the function

if __name__ == "__main__":
    main()


