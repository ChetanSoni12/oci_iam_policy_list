#!/usr/bin/env python3

import oci
import csv

def list_policies_to_csv(output_file="oci_iam_policies.csv", config_profile="DEFAULT"):
    config = oci.config.from_file(profile_name=config_profile)
    identity_client = oci.identity.IdentityClient(config)
    tenancy_id = config['tenancy']

    # Get all compartments including tenancy
    compartments = oci.pagination.list_call_get_all_results(
        identity_client.list_compartments,
        compartment_id=tenancy_id,
        compartment_id_in_subtree=True,
        access_level='ANY'
    ).data

    # Add root compartment
    compartments.append(identity_client.get_compartment(tenancy_id).data)

    print(f"Found {len(compartments)} compartments. Writing policies to CSV...")

    # Counters
    total_policy_count = 0
    total_statement_count = 0
    compartment_policy_summary = {}

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            'Compartment Name',
            'Compartment OCID',
            'Policy Name',
            'Policy Description',
            'Statements'
        ])

        for compartment in compartments:
            policies = oci.pagination.list_call_get_all_results(
                identity_client.list_policies,
                compartment_id=compartment.id
            ).data

            policy_count = len(policies)
            statement_count = 0

            for policy in policies:
                statements_combined = "\n".join(policy.statements)

                writer.writerow([
                    compartment.name,
                    compartment.id,
                    policy.name,
                    policy.description or "",
                    statements_combined
                ])

                statement_count += len(policy.statements)

            compartment_policy_summary[compartment.name] = {
                "policy_count": policy_count,
                "statement_count": statement_count
            }

            total_policy_count += policy_count
            total_statement_count += statement_count

            print(
                f"Compartment: {compartment.name}, "
                f"Policies: {policy_count}, "
                f"Statements: {statement_count}"
            )

    print("\n--- Policy Count Summary ---")
    for comp_name, counts in compartment_policy_summary.items():
        print(
            f"{comp_name}: "
            f"{counts['policy_count']} policies, "
            f"{counts['statement_count']} statements"
        )

    print(f"\nTotal policies across tenancy: {total_policy_count}")
    print(f"Total policy statements across tenancy: {total_statement_count}")
    print(f"\nExport completed. CSV file saved as '{output_file}'.")

if __name__ == "__main__":
    list_policies_to_csv()
