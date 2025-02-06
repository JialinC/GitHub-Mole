{
  repository(owner: "OWNER", name: "REPO") {
    defaultBranchRef {
      target {
        ... on Commit {
          history(first: 100) {  # Adjust 'first' to get more commits per request
            edges {
              node {
                oid  # Commit SHA (OID)
              }
            }
            pageInfo {
              hasNextPage
              endCursor
            }
          }
        }
      }
    }
  }
}

"""Initializes a paginated query for repository commits with specific fields and pagination controls."""
        node_to_use = NODE_DEFAULT_BRANCH_REF if use_default_branch else NODE_REPOSITORY
        super().__init__(
            fields=[
                QueryNode(
                    node_to_use,
                    args={
                        ARG_OWNER: owner,
                        ARG_NAME: repo_name,
                    },