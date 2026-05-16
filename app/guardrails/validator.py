class RecommendationValidator:

    def validate_recommendations(
        self,
        recommendations,
        max_items=10
    ):

        validated = []

        seen_urls = set()

        for rec in recommendations:

            name = rec.get("name", "").strip()
            url = rec.get("url", "").strip()
            test_type = rec.get(
                "test_type",
                ""
            ).strip()

            # -------------------------
            # Required Fields
            # -------------------------

            if not name or not url:
                continue

            # -------------------------
            # SHL URL Validation
            # -------------------------

            if not url.startswith(
                "https://www.shl.com/products/product-catalog/view/"
            ):
                continue

            # -------------------------
            # Deduplication
            # -------------------------

            if url in seen_urls:
                continue

            seen_urls.add(url)

            validated.append({
                "name": name,
                "url": url,
                "test_type": test_type
            })

            # -------------------------
            # Assignment Constraint
            # -------------------------

            if len(validated) >= max_items:
                break

        return validated