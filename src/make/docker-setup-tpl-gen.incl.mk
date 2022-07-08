.PHONY: do-tpl-gen ## @-> apply the environment cnf file into the templates on the tpl-gen container
do-tpl-gen: demand_var-ORG demand_var-ENV demand_var-APP
	docker exec \
	  -e APP=$(APP) \
	  -e ORG=$(ORG) \
	  -e ENV=$(ENV) \
	  -e TGT_PROJ_DIR=$(TGT_PROJ_DIR) \
	  -e TGT_FILE_PATH=$(TGT_FILE_PATH) \
	  -e JSON_CNF_FILE=$(JSON_CNF_FILE) \
	  -e TPL_DIR=$(TPL_DIR) \
	  ${PRODUCT}-tpl-gen-con make tpl-gen

# eof file: src/make/local-setup-tasks.incl.mk
