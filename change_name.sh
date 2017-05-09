git filter-branch -f --commit-filter '
                GIT_COMMITTER_NAME="Kathryn Rowe";
                GIT_AUTHOR_NAME="Kathryn Rowe";
                GIT_COMMITTER_EMAIL="kjrowe06@gmail.com";
                GIT_AUTHOR_EMAIL="kjrowe06@gmail.com";
                git commit-tree "$@";
        ' HEAD