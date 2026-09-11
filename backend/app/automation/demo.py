from .registry import build_default_engine


if __name__ == "__main__":
    engine = build_default_engine()
    run = engine.run(
        "upvc.normalize_enquiry",
        {
            "customer_name": "Demo Customer",
            "phone": "+91XXXXXXXXXX",
            "width_mm": 1200,
            "height_mm": 1500,
            "glass": "double",
            "finish": "white",
        },
    )
    print(run.status.value)
    print(run.output_data)
