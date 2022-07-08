#!/bin/bash

do_zip_till_commit(){


   do_require_var COMMIT "${COMMIT:-}"
   do_require_var TGT_PROJ_DIR "${TGT_PROJ_DIR:-}"
 
   cd "${TGT_PROJ_DIR:-}" || do_log "FATAL cannot cd to TGT_PROJ_DIR: ${TGT_PROJ_DIR:-}"
   cd "${TGT_PROJ_DIR:-}" || exit 1

   git stash
   current_branch=$(git rev-parse --abbrev-ref HEAD)
   zip_name=$(basename "${TGT_PROJ_DIR:-}")


   test -f ../$zip_name.zip && rm -v ../$zip_name.zip

   while read -r c; do 
      c=$(echo "$c"|xargs)
      if [ "$c" == "$COMMIT" ]; then
         git checkout $c
         while read -r f; do
            test "$f" == 'src/bash/run/zip-till-commit.func.sh' && continue
            zip -y ../"$zip_name".zip  "$f" -x './.git/*'
         done < <(git show --pretty="" --name-only "$c")
     fi


   done < <(git log --date=iso --pretty --format="%h")
   
   git checkout $current_branch
   git stash pop

   export exit_code=0
   
}
