SELECT
	CO_CODE,
	COMPANY,
	TRANS,
	DOC_YEAR,
	DOC_MONTH,
	DOCNUM,
	LINE_NO,
	MATERIAL_NO,
	ISBN,
	TITLE,
	MAT_GROUP1,
	MAT_GROUP2,
	MAT_GROUP3,
	DISCIPLINE,
	DOC_DATE,
	POSTING_DATE,
	CUST_CODE,
	CUSTOMER,
	SALES_GROUP,
	CUST_GROUP1,
	CUST_GROUP2,
	CUST_GROUP3,
	CUR,
	DIST,
	WERKS,
	PLANT,
	LOC_CODE,
	LOCATION,
	DISTRICT,
	REGION,
	SALES_PLANT,
	PROFIT_CENTER,
	AE_CODE,
	AE,
	TERM,
	DOC_TYPE,
	PRICE,
	QTY,
	SALES,
	NETSALES,
	SI_NUM,
	SI_DATE,
	COST,
	PRODH
FROM
	ACCPAC.MIS.dbo.TOTALSALES_2
WHERE
	CO_CODE = '1000'
	AND CAST(DOC_YEAR AS NVARCHAR) + 
		CAST(DOC_MONTH AS NVARCHAR) = ?