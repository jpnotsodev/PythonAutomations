SELECT 
	CONVERT(BIGINT, udv_MaterialMaster_CL01.MATNR) AS [Material Number],
	udv_MaterialMaster_CL01.EAN11 AS [ISBN],
	udv_MaterialMaster_CL01.ZZAUTHOR1 + 
		udv_MaterialMaster_CL01.ZZAUTHOR2 + 
		udv_MaterialMaster_CL01.ZZAUTHOR2 AS [Author],
	udv_MaterialMaster_CL01.ZZPUBLISHER1 + 
		udv_MaterialMaster_CL01.ZZPUBLISHER2 +
		udv_MaterialMaster_CL01.ZZPUBLISHER3 AS [Publisher],
	udv_MaterialMaster_CL01.ZZCOPYRIGHT AS [Copyright],
	udv_MaterialMaster_CL01.ZEIVR AS [Edition],
	CONVERT(DECIMAL(10, 2), CASE WHEN udv_MaterialMaster_CL01.KBETR IS NULL
			THEN 0
		ELSE udv_MaterialMaster_CL01.KBETR END) AS [CE Price],
	[Inventory Type] = CASE WHEN CHARINDEX('-', matgroup4_text.BEZEI) = 0 THEN RTRIM(LTRIM(matgroup4_text.BEZEI)) 
		ELSE RTRIM(LTRIM(SUBSTRING(matgroup4_text.BEZEI, 1, CHARINDEX('-', matgroup4_text.BEZEI) - 1))) END,
	[Discount] = CASE WHEN CHARINDEX('-', matgroup4_text.BEZEI) = 0 THEN ''
		ELSE RTRIM(LTRIM(SUBSTRING(matgroup4_text.BEZEI, CHARINDEX('-', matgroup4_text.BEZEI) + 1, LEN(matgroup4_text.BEZEI)))) END,
	-- matgroup2_text.BEZEI AS [Account Set],
	udv_MaterialMaster_CL01.ZZIMPRINT AS [Imprint],
	udv_MaterialMaster_CL01.LABOR AS [Discipline],
	udv_MaterialMaster_CL01.WRKST AS [Subject],
	udv_MaterialMaster_CL01.BRGEW AS [Gross Weight],
	udv_MaterialMaster_CL01.GEWEI AS [Unit Weight],
	udv_MaterialMaster_CL01.ZZPAGENUM AS [Number of Pages],
	udv_MaterialMaster_CL01.MAGRV AS [Binding Type],
	udv_MaterialMaster_CL01.ZEIAR AS [Paper Type],
	udv_MaterialMaster_CL01.MAKTX AS [Short Description],
	prodh_mapping_table.PRODH AS [Product Hierarchy],
	[Product Group] = CASE WHEN CHARINDEX('-', prodh_description.VTEXT) = 0 THEN ''
		ELSE LEFT(LTRIM(prodh_description.VTEXT), 3) END
	-- [Product Classification] = CASE WHEN CHARINDEX('-', prodh_description.VTEXT) = 0 THEN ''
	--	ELSE UPPER(LEFT(LTRIM(REPLACE(RIGHT(RTRIM(prodh_description.VTEXT), LEN(prodh_description.VTEXT) - 4), '-', '')), 1)) + 
	--		RIGHT(LTRIM(REPLACE(RIGHT(RTRIM(prodh_description.VTEXT), LEN(prodh_description.VTEXT) - 4), '-', '')), LEN(LTRIM(REPLACE(RIGHT(RTRIM(prodh_description.VTEXT), LEN(prodh_description.VTEXT) - 4), '-', ''))) - 1) END
FROM 
	prd.udv_MaterialMaster_CL01
		LEFT JOIN
			(SELECT 
				DISTINCT MANDT,
				MATNR,
				PRODH
			FROM 
				prd.MVKE 
			WHERE
				MANDT = 888
				AND VTWEG = '11') prodh_mapping_table
		ON
			prodh_mapping_table.MATNR = prd.udv_MaterialMaster_CL01.MATNR	
			AND prodh_mapping_table.MANDT = prd.udv_MaterialMaster_CL01.MANDT
		LEFT JOIN
			(SELECT 
				prodh_head.PRODH, 
				prodh_text.VTEXT
			FROM
				prd.T179 prodh_head,
				prd.T179T prodh_text
			WHERE
				prodh_head.MANDT = prodh_text.MANDT
				AND prodh_head.PRODH = prodh_text.PRODH
				AND prodh_head.MANDT = '888'
				AND prodh_text.SPRAS = 'E') prodh_description
		ON
			prodh_description.PRODH = prodh_mapping_table.PRODH
		LEFT JOIN
			prd.TVM4T matgroup4_text
		ON
			matgroup4_text.MVGR4 = udv_MaterialMaster_CL01.MVGR4
			AND matgroup4_text.MANDT = udv_MaterialMaster_CL01.MANDT
		LEFT JOIN
			prd.TVM2T matgroup2_text
		ON
			matgroup2_text.MVGR2 = udv_MaterialMaster_CL01.MVGR2
			AND matgroup2_text.MANDT = udv_MaterialMaster_CL01.MANDT