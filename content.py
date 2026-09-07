"""
Content generation module for ProFlow Plumbing.
Provides varied intro text, H1 variants, and regional FAQ sets
to ensure no two city pages read as identical templates.
"""

import hashlib

# === STATE NAME MAP ===
STATE_NAMES = {
    'AZ': 'Arizona', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'ID': 'Idaho', 'IL': 'Illinois',
    'IN': 'Indiana', 'MA': 'Massachusetts', 'MD': 'Maryland', 'MN': 'Minnesota',
    'MS': 'Mississippi', 'NJ': 'New Jersey', 'NY': 'New York', 'OH': 'Ohio',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'SC': 'South Carolina', 'TN': 'Tennessee',
    'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'WA': 'Washington'
}

# === REGION MAP (for regional FAQ variation) ===
STATE_REGIONS = {
    'AZ': 'southwest', 'CO': 'mountain', 'CT': 'northeast', 'DE': 'northeast',
    'FL': 'southeast', 'GA': 'southeast', 'ID': 'mountain', 'IL': 'midwest',
    'IN': 'midwest', 'MA': 'northeast', 'MD': 'northeast', 'MN': 'midwest',
    'MS': 'southeast', 'NJ': 'northeast', 'NY': 'northeast', 'OH': 'midwest',
    'OR': 'pacific', 'PA': 'northeast', 'SC': 'southeast', 'TN': 'southeast',
    'TX': 'southwest', 'UT': 'mountain', 'VA': 'southeast', 'WA': 'pacific'
}

# === REGIONAL CONTEXT (climate/plumbing factors) ===
REGIONAL_CONTEXT = {
    'northeast': 'Winters here bring freezing temperatures that put stress on pipes. Older homes in the area often have aging plumbing that needs regular attention.',
    'southeast': 'The warm climate and hurricane season mean plumbing systems here deal with heavy rain, humidity, and occasional flooding.',
    'midwest': 'Cold winters and hard water are common challenges for plumbing in this region. Pipe insulation and water softening can make a real difference.',
    'southwest': 'Hot summers and dry conditions mean plumbing systems here need to handle high demand and mineral-heavy water.',
    'mountain': 'High altitude and cold winters create unique plumbing challenges. Frozen pipes and water pressure changes are common issues.',
    'pacific': 'Mild but wet winters and seismic activity mean plumbing here needs to be built to handle both moisture and movement.'
}

# === H1 VARIANTS (12 unique structures) ===
H1_VARIANTS = [
    "Plumbing Services in {city}, {state}",
    "Plumbers in {city}, {state}",
    "{city}, {state} Plumbing Services",
    "Local Plumbers Serving {city}, {state}",
    "Plumbing Help in {city}, {state}",
    "{city} Plumbing",
    "Reliable Plumbing in {city}, {state}",
    "Plumbers Near You in {city}, {state}",
    "{city}, {state} Local Plumbing",
    "Professional Plumbing for {city}, {state}",
    "Plumbing Repair in {city}, {state}",
    "Emergency and Routine Plumbing in {city}, {state}"
]

# === INTRO VARIANTS (20 unique paragraph structures) ===
# Each uses {city}, {state}, {state_name}, {region_context} placeholders
INTRO_VARIANTS = [
    "When you need a plumber in {city}, we can help. Our network connects you with licensed plumbing professionals who serve the {city} area. From leaky faucets to burst pipes, we handle it all.",
    "Looking for a plumber in {city}, {state}? We work with local licensed plumbers who know the area. Whether it is a small drip or a major repair, we are here to help.",
    "Plumbing problems do not wait for a convenient time. That is why our network of plumbers in {city} is ready when you need them. Call us for fast service from licensed professionals.",
    "We connect homeowners in {city} with licensed plumbers who get the job done right. {region_context} Our team is ready for everything from routine maintenance to emergency repairs.",
    "Need plumbing help in {city}, {state}? We can put you in touch with a local plumber who knows the area. {region_context} Call us today for fast, reliable service.",
    "Our plumbing network covers {city} and the surrounding area. We work with licensed and insured plumbers who handle residential plumbing of all kinds. Give us a call and we will find the right pro for your job.",
    "If you live in {city} and need a plumber, you are in the right place. We connect you with licensed local professionals who can handle leaks, clogs, water heaters, and more.",
    "Plumbing issues in {city}? We have you covered. Our network includes licensed plumbers who serve this part of {state_name}. {region_context} Call now for a fast connection to a local pro.",
    "We help homeowners in {city}, {state} find reliable plumbing service. Whether your water heater quit or a pipe is leaking, our network of licensed plumbers can help. {region_context}",
    "From drain cleaning to water heater repair, our plumbing network serves {city} and the surrounding communities. We work with licensed professionals who offer upfront pricing and fast response.",
    "Got a plumbing problem in {city}? Do not wait for it to get worse. We connect you with licensed plumbers in {state_name} who can assess the issue and fix it properly.",
    "Our service connects {city} homeowners with experienced, licensed plumbers. {region_context} We handle everything from minor leaks to full pipe replacements.",
    "We serve {city}, {state} with access to a network of licensed plumbing professionals. {region_context} Call us and we will connect you with someone who can help today.",
    "Finding a good plumber in {city} should not be hard. We make it simple by connecting you with licensed local plumbers who do quality work. {region_context}",
    "Homeowners in {city} count on our network for reliable plumbing service. We partner with licensed plumbers who handle repairs, installations, and emergencies throughout {state_name}.",
    "If your plumbing is acting up in {city}, {state}, give us a call. We will connect you with a licensed plumber who serves your area. No job is too big or too small.",
    "We bring {city} residents access to licensed plumbing professionals. {region_context} Whether you need a simple fix or a major repair, our network has you covered.",
    "Plumbing repairs in {city} do not have to be a hassle. We connect you with licensed plumbers who show up on time and do the work right. {region_context}",
    "Our plumbing service network extends to {city} and across {state_name}. We work with licensed and insured plumbers who provide honest, straightforward service for homeowners.",
    "When plumbing goes wrong in {city}, we help you find the right fix. Our network includes licensed plumbers who handle residential work of every kind. {region_context} Call us and get connected fast."
]

# === FAQ SETS ===
# General FAQs (used across all regions, with variations)
GENERAL_FAQS = [
    {
        "question": "How quickly can a plumber get to my home?",
        "answer": "Response times vary by location and time of day. In most cases, our network can connect you with a plumber who can come out the same day or next day. For emergencies like burst pipes, we prioritize getting someone to you as fast as possible."
    },
    {
        "question": "Are the plumbers in your network licensed and insured?",
        "answer": "Yes. Every plumber in our network holds proper state licensing and carries insurance. We verify credentials before adding any professional to our service area."
    },
    {
        "question": "How much does a typical plumbing repair cost?",
        "answer": "Costs depend on the type of repair, the parts needed, and the complexity of the job. We recommend getting a clear estimate before any work begins. The plumbers in our network provide upfront pricing so you know what to expect."
    },
    {
        "question": "Do you handle emergency plumbing calls?",
        "answer": "Yes. Plumbing emergencies like burst pipes, major leaks, and sewer backups need fast attention. Call us and we will connect you with a plumber who can respond quickly."
    },
    {
        "question": "What areas do you serve?",
        "answer": "We serve {city} and the surrounding communities in {state_name}. Our network covers {state_count} states and thousands of cities. If you are in our service area, we can connect you with a local plumber."
    }
]

# Region-specific FAQ additions
REGIONAL_FAQS = {
    'northeast': [
        {
            "question": "How do I protect my pipes from freezing in the winter?",
            "answer": "Insulate exposed pipes in basements, crawl spaces, and exterior walls. Let faucets drip during extreme cold snaps. Keep your thermostat set to at least 55 degrees even when you are away. If a pipe does freeze, call a plumber right away before it bursts."
        },
        {
            "question": "My old home has outdated plumbing. Should I repipe?",
            "answer": "Many older homes in the northeast have galvanized steel or even lead pipes that corrode over time. If you are seeing discolored water, low pressure, or frequent leaks, a repipe might be worth considering. A licensed plumber can inspect your system and advise you."
        }
    ],
    'southeast': [
        {
            "question": "How do I prepare my plumbing for hurricane season?",
            "answer": "Before a storm, know where your main water shutoff valve is. Clear gutters and downspouts so water drains away from your foundation. If flooding is expected, turn off your water heater and main water supply. After the storm, check for leaks and water damage before turning everything back on."
        },
        {
            "question": "What causes slow drains in this area?",
            "answer": "Tree roots, grease buildup, and mineral deposits are common causes. The warm climate also means more organic material can break down inside pipes. Regular drain cleaning helps prevent major blockages."
        }
    ],
    'midwest': [
        {
            "question": "How do I deal with hard water in my home?",
            "answer": "Hard water is common across the midwest and causes mineral buildup in pipes, water heaters, and fixtures. A water softener can help protect your plumbing and appliances. A plumber can test your water hardness and recommend the right system."
        },
        {
            "question": "What should I do if my pipes freeze?",
            "answer": "Turn off your main water supply right away. Open the affected faucets to relieve pressure. Apply gentle heat to the frozen section using a hair dryer or heating pad. Never use an open flame. If the pipe has burst, call a plumber immediately."
        }
    ],
    'southwest': [
        {
            "question": "How does hard water affect my plumbing out here?",
            "answer": "The mineral content in southwest water can build up inside pipes and water heaters over time. This reduces water flow and efficiency. A water softener or regular descaling can help. A plumber can assess your system and recommend solutions."
        },
        {
            "question": "What plumbing issues are common in hot, dry climates?",
            "answer": "High water demand during summer puts stress on pipes and fixtures. Soil shifting from heat and drought can also affect underground lines. Regular inspections help catch problems before they turn into expensive repairs."
        }
    ],
    'mountain': [
        {
            "question": "How do I prevent frozen pipes at high altitude?",
            "answer": "Insulate all exposed pipes, especially in crawl spaces and garages. Use heat tape on vulnerable sections. Keep cabinet doors open under sinks to let warm air circulate. During extreme cold, let faucets drip slightly to keep water moving."
        },
        {
            "question": "Does altitude affect water pressure in my plumbing?",
            "answer": "Yes. Higher elevations can cause lower water pressure. If your pressure is consistently low, a plumber can check for issues like partially closed valves, corroded pipes, or the need for a pressure booster system."
        }
    ],
    'pacific': [
        {
            "question": "How do I protect my plumbing from earthquake damage?",
            "answer": "Make sure your water heater is strapped and secured. Flexible gas and water connections can help prevent breaks during seismic activity. Know where your main shutoff valves are. After any significant quake, check for leaks and call a plumber if you spot damage."
        },
        {
            "question": "What causes pipe corrosion in the Pacific Northwest?",
            "answer": "The wet climate and soil conditions can accelerate corrosion in underground pipes. Older homes may have galvanized steel pipes that are nearing the end of their lifespan. A plumber can inspect your system and recommend repairs or replacement if needed."
        }
    ]
}

# Additional varied FAQs for rotation
EXTRA_FAQS = [
    {
        "question": "When should I call a plumber instead of trying to fix it myself?",
        "answer": "If the problem involves your main water line, sewer line, gas lines, or anything behind a wall, call a professional. Also call if a simple fix does not work after one or two attempts. Trying to force a repair can make the problem worse and more expensive."
    },
    {
        "question": "How often should I have my plumbing inspected?",
        "answer": "A general inspection every one to two years is a good idea. If your home is older or you have had recurring issues, more frequent checks can catch problems early. A plumber can look at pipes, fixtures, the water heater, and drainage."
    },
    {
        "question": "What is the most common plumbing repair?",
        "answer": "Clogged drains and running toilets are among the most common calls. Leaky faucets and water heater issues are also very frequent. Most of these are straightforward repairs for a licensed plumber."
    },
    {
        "question": "How do I know if I have a hidden water leak?",
        "answer": "Watch for signs like unexplained increases in your water bill, damp spots on walls or floors, mold or mildew smells, and the sound of running water when nothing is turned on. A plumber can do a pressure test to confirm a hidden leak."
    },
    {
        "question": "Can a plumber help with low water pressure?",
        "answer": "Yes. Low water pressure can be caused by clogged aerators, corroded pipes, a failing pressure regulator, or issues with the municipal supply. A plumber can diagnose the cause and fix it."
    }
]


def get_hash_index(text, modulo):
    """Generate a stable hash-based index for consistent variant selection."""
    h = hashlib.md5(text.encode()).hexdigest()
    return int(h[:8], 16) % modulo


def get_h1(city, state_code):
    """Get a varied H1 for a city page."""
    idx = get_hash_index(f"{city}-{state_code}-h1", len(H1_VARIANTS))
    return H1_VARIANTS[idx].format(
        city=city,
        state=STATE_NAMES.get(state_code, state_code)
    )


def get_intro(city, state_code):
    """Get a varied intro paragraph for a city page."""
    state_name = STATE_NAMES.get(state_code, state_code)
    region = STATE_REGIONS.get(state_code, 'northeast')
    region_context = REGIONAL_CONTEXT.get(region, '')
    
    idx = get_hash_index(f"{city}-{state_code}-intro", len(INTRO_VARIANTS))
    return INTRO_VARIANTS[idx].format(
        city=city,
        state=state_code,
        state_name=state_name,
        region_context=region_context
    )


def get_faqs(city, state_code, state_city_count):
    """Get 4-5 FAQs for a city page, mixing general and regional."""
    state_name = STATE_NAMES.get(state_code, state_code)
    region = STATE_REGIONS.get(state_code, 'northeast')
    
    # Select 2-3 general FAQs based on hash
    base_idx = get_hash_index(f"{city}-{state_code}-faq", len(GENERAL_FAQS))
    selected_general = []
    for i in range(3):
        faq_idx = (base_idx + i) % len(GENERAL_FAQS)
        faq = GENERAL_FAQS[faq_idx].copy()
        # Fill in placeholders
        faq['question'] = faq['question'].format(city=city, state_name=state_name)
        faq['answer'] = faq['answer'].format(
            city=city,
            state_name=state_name,
            state_count=len(STATE_NAMES)
        )
        selected_general.append(faq)
    
    # Add 1-2 regional FAQs
    regional = REGIONAL_FAQS.get(region, REGIONAL_FAQS['northeast'])
    regional_idx = get_hash_index(f"{city}-{state_code}-regional", len(regional))
    selected_regional = [regional[regional_idx]]
    
    # Sometimes add an extra FAQ for variety
    extra_idx = get_hash_index(f"{city}-{state_code}-extra", len(EXTRA_FAQS))
    if get_hash_index(f"{city}-{state_code}-hasextra", 3) == 0:
        selected_general.append(EXTRA_FAQS[extra_idx])
    
    return selected_general + selected_regional


def slugify(text):
    """Convert text to URL-friendly slug."""
    import re
    slug = text.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')
