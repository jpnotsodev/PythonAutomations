SELECT
	prd.EKPO.BUKRS AS [Company Code],
	prd.EKPO.EBELN AS [Purchase Order No],
	CAST(prd.EKKO.AEDAT AS DATE) AS [Purchase Order Date],
	[Document Type] = (SELECT 
							BATXT 
						FROM
							prd.T161T
						WHERE
							BSART = prd.EKKO.BSART
							AND MANDT = '888'
							AND SPRAS = 'E'),
	CONVERT(BIGINT, prd.EKKO.LIFNR) AS [Vendor Code],
	prd.LFA1.NAME1 + 
		NAME2 + 
			NAME3 + 
				NAME4 AS [Vendor Name],
	prd.EKPO.NETPR AS [Unit Cost under GR Currency],
	CONVERT(INT, prd.EKPO.MENGE) AS [GR Qty],
	prd.EKPO.MATNR AS [Material No],
	prd.EKPO.NETWR AS [Amount in FOREX],
	[Storage Location] = (SELECT 
							LGOBE
						FROM
							prd.T001L
						WHERE
							WERKS = prd.EKPO.WERKS
							AND LGORT = prd.EKPO.LGORT
							AND MANDT = '888'),
	EKBE.WAERS AS [Currency],
	[Exchange Rate] = CASE WHEN EKBE.WAERS ='PHP' THEN 1 
						ELSE (SELECT 
								UKURS
							FROM
								prd.ZPR_TCURR_HIST
							WHERE
								FCURR = EKBE.WAERS
								AND DATE_ADDED = prd.EKKO.BEDAT) END,
	[Amount in PHP] = CASE WHEN EKBE.WAERS ='PHP' THEN CONVERT(DECIMAL(10, 2), (prd.EKPO.MENGE * prd.EKPO.NETPR) * 1)
						ELSE (SELECT 
								CONVERT(DECIMAL(10, 2), (prd.EKPO.MENGE * prd.EKPO.NETPR) * UKURS)
							FROM
								prd.ZPR_TCURR_HIST
							WHERE
								FCURR = EKBE.WAERS
								AND DATE_ADDED = prd.EKKO.BEDAT) END,
	EKBE.EBELP AS [Line No],
	EKBE.BELNR AS [GR Doc No],
	CAST(EKBE.BUDAT AS DATE) AS [GR Date]
FROM
	-- Purchasing Document Header
	prd.EKPO
		JOIN
			-- Purchasing Document Item
			prd.EKKO
		ON
			prd.EKPO.EBELN = prd.EKKO.EBELN
			AND prd.EKPO.MANDT = prd.EKPO.MANDT
		JOIN
			-- Vendor Master List
			prd.LFA1
		ON
			prd.LFA1.LIFNR = prd.EKKO.LIFNR
			AND prd.LFA1.MANDT = prd.EKPO.MANDT
		JOIN
			-- History per Purchasing Document
			(SELECT 
				*
			FROM
				prd.EKBE
			WHERE				
				prd.EKBE.ELIKZ = 'X' -- Delivery Completed Indicator
				AND prd.EKBE.MANDT = '888') EKBE
		ON
			prd.EKPO.EBELN = EKBE.EBELN
			AND prd.EKKO.MANDT = EKBE.MANDT
			AND prd.EKPO.EBELP = EKBE.EBELP
WHERE
	prd.EKPO.MANDT = '888'
	--AND prd.EKPO.ELIKZ = 'X' -- Delivery Completed Indicator
	AND prd.EKPO.WEPOS = 'X' -- Goods Receipt Indicator
	AND (NOT prd.EKPO.LOEKZ = 'L' -- Deletion Indicator
		OR prd.EKPO.LOEKZ = '')
	AND LEFT(EKBE.BUDAT, 6) = ? = ? -- Indicates that the 
	AND prd.EKPO.RETPO <> 'X'
	AND LEFT(prd.EKPO.EBELN, 2) NOT IN ('79', '55', '45')