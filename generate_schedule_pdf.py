# generate_schedule_pdf.py
import random
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Attempt to register a common font, handle if not found
try:
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf')) # Common font
    FONT_NAME = 'Arial'
    FONT_NAME_BOLD = 'Arial-Bold' # ReportLab often uses -Bold for bold variant
    pdfmetrics.registerFont(TTFont(FONT_NAME_BOLD, 'arialbd.ttf'))
except:
    print("Arial font not found, using Helvetica.")
    FONT_NAME = 'Helvetica'
    FONT_NAME_BOLD = 'Helvetica-Bold'


# Import data from the other file
try:
    from schedule_data import COURSE_DATA, TIMESLOT_DEFINITIONS, DAYS_OF_WEEK
except ImportError:
    print("Error: schedule_data.py not found or contains errors. Please ensure it's in the same directory.")
    exit()

# Import genetic algorithm components
try:
    from genetic_algorithm_scheduler import GeneticScheduler, Alocacao, Horario, Sala
except ImportError:
    print("Error: genetic_algorithm_scheduler.py not found. Please ensure it's in the same directory.")
    exit()

# --- Configuration ---
PDF_FILENAME = "horario_gerado.pdf"
PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)

MARGIN_TOP = 1.2 * cm
MARGIN_BOTTOM = 1.0 * cm
MARGIN_LEFT = 0.8 * cm
MARGIN_RIGHT = 0.8 * cm

HEADER_HEIGHT = 1.8 * cm # For "CC: X Periodo" and institute name
FOOTER_HEIGHT = 0.6 * cm
DAY_LABEL_WIDTH = 2.0 * cm  # Increased for better readability
TIMESLOT_HEADER_HEIGHT = 1.8 * cm # Increased for better time slot labels

GRID_X_START = MARGIN_LEFT + DAY_LABEL_WIDTH
GRID_Y_START = PAGE_HEIGHT - MARGIN_TOP - HEADER_HEIGHT - TIMESLOT_HEADER_HEIGHT
GRID_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT - DAY_LABEL_WIDTH
GRID_HEIGHT = PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - HEADER_HEIGHT - FOOTER_HEIGHT - TIMESLOT_HEADER_HEIGHT

ROW_HEIGHT = GRID_HEIGHT / len(DAYS_OF_WEEK)

# Calculate column widths: regular slots are wider than interval slots
NUM_REGULAR_SLOTS = sum(1 for _, _, _, is_interval in TIMESLOT_DEFINITIONS if not is_interval)
NUM_INTERVAL_SLOTS = sum(1 for _, _, _, is_interval in TIMESLOT_DEFINITIONS if is_interval)
REGULAR_SLOT_RELATIVE_WIDTH = 1.0
INTERVAL_SLOT_RELATIVE_WIDTH = 0.4 # Increased intervals width for better visibility

TOTAL_RELATIVE_WIDTH_UNITS = (NUM_REGULAR_SLOTS * REGULAR_SLOT_RELATIVE_WIDTH) + \
                             (NUM_INTERVAL_SLOTS * INTERVAL_SLOT_RELATIVE_WIDTH)

REGULAR_COL_WIDTH = (GRID_WIDTH / TOTAL_RELATIVE_WIDTH_UNITS) * REGULAR_SLOT_RELATIVE_WIDTH
INTERVAL_COL_WIDTH = (GRID_WIDTH / TOTAL_RELATIVE_WIDTH_UNITS) * INTERVAL_SLOT_RELATIVE_WIDTH

# Store column properties (x-position, width, and original slot_id)
COLUMN_PROPERTIES = []
current_x = GRID_X_START
for slot_id, _, _, is_interval in TIMESLOT_DEFINITIONS:
    col_w = INTERVAL_COL_WIDTH if is_interval else REGULAR_COL_WIDTH
    COLUMN_PROPERTIES.append({'id': slot_id, 'x': current_x, 'width': col_w})
    current_x += col_w

SLOT_ID_TO_INDEX = {slot['id']: i for i, slot in enumerate(COLUMN_PROPERTIES)}

# --- Styles ---
styles = getSampleStyleSheet()
TITLE_STYLE = ParagraphStyle(
    'TitleStyle', parent=styles['h1'], fontName=FONT_NAME_BOLD, fontSize=16, alignment=TA_LEFT, spaceAfter=0.1*cm
)
LOCATION_STYLE = ParagraphStyle(
    'LocationStyle', parent=styles['Normal'], fontName=FONT_NAME, fontSize=10, alignment=TA_LEFT, spaceAfter=0.3*cm
)
DAY_LABEL_STYLE = ParagraphStyle(
    'DayLabelStyle', parent=styles['Normal'], fontName=FONT_NAME_BOLD, fontSize=11, alignment=TA_CENTER, leading=12
)
TIMESLOT_LABEL_STYLE = ParagraphStyle(
    'TimeslotLabelStyle', parent=styles['Normal'], fontName=FONT_NAME, fontSize=8, alignment=TA_CENTER, leading=9
)
COURSE_TEXT_STYLE = ParagraphStyle(
    'CourseStyle', parent=styles['Normal'], fontName=FONT_NAME, fontSize=8, textColor=colors.black,
    alignment=TA_CENTER, leading=9
)
FOOTER_STYLE = ParagraphStyle(
    'FooterStyle', parent=styles['Normal'], fontName=FONT_NAME, fontSize=9, alignment=TA_LEFT
)

# --- Color Generation ---
def generate_random_colors(num_colors=64):
    """Generates a list of distinctish random reportlab color objects."""
    color_list = []
    for _ in range(num_colors):
        # Generate colors with good perceived brightness difference
        r = random.uniform(0.5, 1.0) # Brighter colors
        g = random.uniform(0.5, 1.0)
        b = random.uniform(0.5, 1.0)
        color_list.append(colors.Color(r, g, b)) # Solid colors (no alpha/transparency)
    return color_list

COLOR_PALETTE = generate_random_colors()
COLOR_IDX_GENERATOR = (i for i in range(len(COLOR_PALETTE))) # Infinite loop if needed, but we have 64

def get_next_color():
    """Cycles through the color palette."""
    global COLOR_IDX_GENERATOR
    try:
        idx = next(COLOR_IDX_GENERATOR)
    except StopIteration: # Reset generator if exhausted
        COLOR_IDX_GENERATOR = (i for i in range(len(COLOR_PALETTE)))
        idx = next(COLOR_IDX_GENERATOR)
    return COLOR_PALETTE[idx % len(COLOR_PALETTE)]


# --- Drawing Functions ---
def draw_page_template(c: canvas.Canvas, title_text: str, location_text: str):
    """Draws the static elements of a page: headers, footers, grid lines."""
    c.setFont(FONT_NAME, 10)

    # 1. Page Title and Location
    p_title = Paragraph(title_text, TITLE_STYLE)
    title_width, title_height = p_title.wrap(PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT, HEADER_HEIGHT)
    p_title.drawOn(c, MARGIN_LEFT, PAGE_HEIGHT - MARGIN_TOP - title_height)

    p_location = Paragraph(location_text, LOCATION_STYLE)
    location_width, location_height = p_location.wrap(PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT, HEADER_HEIGHT - title_height)
    p_location.drawOn(c, MARGIN_LEFT, PAGE_HEIGHT - MARGIN_TOP - title_height - location_height - 0.2*cm)
    
    # 2. Footer - Fixed overlapping issue
    footer_text = f"Horário criado: {random.randint(1,28)}/{random.randint(1,12)}/2024"
    p_footer = Paragraph(footer_text, FOOTER_STYLE)
    footer_width, footer_height = p_footer.wrap(GRID_X_START + GRID_WIDTH - MARGIN_LEFT, FOOTER_HEIGHT)
    p_footer.drawOn(c, MARGIN_LEFT, FOOTER_HEIGHT) 

    asc_footer_text = "Algoritmo Genético para Geração de Horários"
    p_asc_footer = Paragraph(asc_footer_text, FOOTER_STYLE)
    asc_width, asc_height = p_asc_footer.wrap(GRID_X_START + GRID_WIDTH - MARGIN_LEFT, FOOTER_HEIGHT + 0.3*cm)
    # Align to the right and at bottom
    p_asc_footer.drawOn(c, PAGE_WIDTH - MARGIN_RIGHT - asc_width, MARGIN_BOTTOM)

    # 3. Grid Lines and Labels
    # Draw grid border
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    
    # Horizontal lines (including header separator)
    c.line(MARGIN_LEFT, GRID_Y_START + TIMESLOT_HEADER_HEIGHT, MARGIN_LEFT + DAY_LABEL_WIDTH + GRID_WIDTH, GRID_Y_START + TIMESLOT_HEADER_HEIGHT)
    for i in range(len(DAYS_OF_WEEK) + 1):
        y = GRID_Y_START - (i * ROW_HEIGHT)
        c.line(MARGIN_LEFT, y, MARGIN_LEFT + DAY_LABEL_WIDTH + GRID_WIDTH, y)

    # Vertical lines (Day label column + timeslot columns)
    c.line(MARGIN_LEFT, GRID_Y_START + TIMESLOT_HEADER_HEIGHT, MARGIN_LEFT, GRID_Y_START - GRID_HEIGHT)
    c.line(GRID_X_START, GRID_Y_START + TIMESLOT_HEADER_HEIGHT, GRID_X_START, GRID_Y_START - GRID_HEIGHT)
    
    for col_prop in COLUMN_PROPERTIES:
        x_line = col_prop['x'] + col_prop['width']
        c.line(x_line, GRID_Y_START + TIMESLOT_HEADER_HEIGHT, x_line, GRID_Y_START - GRID_HEIGHT)

    # Day Labels
    for i, day_name in enumerate(DAYS_OF_WEEK):
        y_pos = GRID_Y_START - (i * ROW_HEIGHT) - ROW_HEIGHT / 2
        p_day = Paragraph(day_name, DAY_LABEL_STYLE)
        w, h = p_day.wrap(DAY_LABEL_WIDTH, ROW_HEIGHT)
        p_day.drawOn(c, MARGIN_LEFT + (DAY_LABEL_WIDTH - w)/2, y_pos - h/2)

    # Timeslot Labels with better formatting
    y_label_base = GRID_Y_START + TIMESLOT_HEADER_HEIGHT
    for col_prop in COLUMN_PROPERTIES:
        slot_id = col_prop['id']
        # Find the original definition for label text
        original_def = next(s_def for s_def in TIMESLOT_DEFINITIONS if s_def[0] == slot_id)
        label_L1 = original_def[1]
        label_L2 = original_def[2]
        
        # Format timeslot header better
        if original_def[3]:  # is_interval
            full_label_text = f"<font size=6>{label_L1}</font><br/><font size=6>{label_L2}</font>"
        else:
            full_label_text = f"<b>{label_L1}</b><br/><font size=7>{label_L2}</font>"
        
        p_slot = Paragraph(full_label_text, TIMESLOT_LABEL_STYLE)
        
        col_width = col_prop['width']
        w, h = p_slot.wrap(col_width, TIMESLOT_HEADER_HEIGHT)
        
        # Center in the column with proper vertical alignment
        p_slot.drawOn(c, col_prop['x'] + (col_width - w) / 2, y_label_base - h - 0.2*cm)


def get_elementary_slots_indices(start_slot_id: str, end_slot_id: str):
    """Returns a list of column indices for all elementary slots between start and end (inclusive)."""
    try:
        start_idx = SLOT_ID_TO_INDEX[start_slot_id]
        end_idx = SLOT_ID_TO_INDEX[end_slot_id]
    except KeyError:
        print(f"Error: Slot ID {start_slot_id} or {end_slot_id} not found in SLOT_ID_TO_INDEX.")
        return []
    
    if start_idx > end_idx: # Should not happen with valid data
        print(f"Warning: start_slot_id {start_slot_id} is after end_slot_id {end_slot_id}.")
        return []
    return list(range(start_idx, end_idx + 1))


def get_course_blocks_with_intervals(start_slot_id: str, end_slot_id: str):
    """
    Returns a list of course blocks, splitting around intervals.
    Each block is a tuple (start_idx, end_idx) of non-interval slots.
    """
    try:
        start_idx = SLOT_ID_TO_INDEX[start_slot_id]
        end_idx = SLOT_ID_TO_INDEX[end_slot_id]
    except KeyError:
        print(f"Error: Slot ID {start_slot_id} or {end_slot_id} not found.")
        return []
    
    if start_idx > end_idx:
        return []
    
    # Find all interval slots within the range
    blocks = []
    current_block_start = start_idx
    
    for i in range(start_idx, end_idx + 1):
        slot_id = COLUMN_PROPERTIES[i]['id']
        # Find if this slot is an interval
        is_interval = False
        for _, _, _, interval_flag in TIMESLOT_DEFINITIONS:
            if _ == slot_id and interval_flag:
                is_interval = True
                break
        
        if is_interval:
            # If we hit an interval, close the current block (if it exists)
            if current_block_start < i:
                blocks.append((current_block_start, i - 1))
            # Skip the interval and start a new block after it
            current_block_start = i + 1
    
    # Add the final block if it exists
    if current_block_start <= end_idx:
        blocks.append((current_block_start, end_idx))
    
    return blocks


def draw_course_block_split(c: canvas.Canvas, day_index: int, start_slot_id: str, end_slot_id: str,
                           course_name: str, teacher_name: str, fill_color):
    """Draws course blocks, splitting around intervals if necessary."""
    
    # Get the blocks, split around intervals
    blocks = get_course_blocks_with_intervals(start_slot_id, end_slot_id)
    
    if not blocks:
        print(f"No valid blocks found for course {course_name}")
        return
    
    for block_start_idx, block_end_idx in blocks:
        # Draw each block separately
        block_x = COLUMN_PROPERTIES[block_start_idx]['x']
        block_y = GRID_Y_START - ((day_index + 1) * ROW_HEIGHT)
        
        block_width = 0
        for i in range(block_start_idx, block_end_idx + 1):
            block_width += COLUMN_PROPERTIES[i]['width']
        
        block_height = ROW_HEIGHT

        # Draw colored rectangle with padding
        padding = 1
        c.setFillColor(fill_color)
        c.setStrokeColor(colors.darkgrey)
        c.rect(block_x + padding, block_y + padding, block_width - 2*padding, block_height - 2*padding, fill=1, stroke=1)

        # Draw text (course name and teacher)
        r, g, b, _ = fill_color.rgba()
        text_color = colors.black
        if (r + g + b) < 1.5:
            text_color = colors.white
        
        course_p_style = ParagraphStyle(
            'CourseBlockStyle', 
            parent=COURSE_TEXT_STYLE, 
            textColor=text_color,
            fontSize=8,
            leading=9,
            alignment=TA_CENTER,
            fontName=FONT_NAME,
            allowWidows=1,
            allowOrphans=1
        )

        # Truncate long course names for better fit
        max_course_name_length = 40
        display_name = course_name if len(course_name) <= max_course_name_length else course_name[:max_course_name_length] + "..."
        
        text_content = f"<font name='{FONT_NAME}'>{display_name}</font><br/><br/><font name='{FONT_NAME_BOLD}'><b>{teacher_name}</b></font>"
        p_course = Paragraph(text_content, course_p_style)
        
        # Calculate available width/height for text, with padding
        text_area_width = block_width - 0.4 * cm
        text_area_height = block_height - 0.3 * cm
        
        # Ensure minimum dimensions
        if text_area_width > 0 and text_area_height > 0:
            w, h = p_course.wrap(text_area_width, text_area_height)
            
            # Center the paragraph in the block
            text_x = block_x + (block_width - w) / 2
            text_y = block_y + (block_height - h) / 2
            p_course.drawOn(c, text_x, text_y)


def convert_genetic_algorithm_result_to_pdf_format(genetic_result):
    """
    Converts genetic algorithm result (List[Alocacao]) to the format expected by PDF generator
    """
    # Day mapping from genetic algorithm format to PDF format
    day_mapping = {
        'Segunda': 'Seg',
        'Terça': 'Ter', 
        'Quarta': 'Qua',
        'Quinta': 'Qui',
        'Sexta': 'Sex'
    }
    
    # Time slot mapping from genetic algorithm format (M1-6, T1-6) to PDF format
    def convert_horario_to_timeslot(horario):
        """Convert Horario object to timeslot format used by PDF generator"""
        return f"{horario.turno}{horario.slot}"
    
    # Initialize periods structure
    periods_data = {}
    for periodo in range(1, 9):
        periods_data[str(periodo)] = {
            "page_title": f"CC: {periodo}º Período",
            "location_info": "Instituto de Computação IC/UFAL, Cidade Universitária, Maceió",
            "courses": []
        }
    
    # Initialize electives structure
    periods_data["Eletivas"] = {
        "page_title_prefix": "CC: Eletivas",
        "location_info": "Instituto de Computação IC/UFAL, Cidade Universitária, Maceió",
        "courses": []
    }
    
    # Group allocations by period
    allocations_by_period = {}
    allocations_eletivas = []
    
    # Import disciplines data to get period info
    try:
        from genetic_algorithm_scheduler import GeneticScheduler
        scheduler = GeneticScheduler()
        disciplinas_dict = {d.nome: d for d in scheduler.disciplinas}
    except:
        print("Warning: Could not load genetic algorithm data for period mapping")
        disciplinas_dict = {}
    
    for allocation in genetic_result:
        # Get period for this discipline
        disciplina_obj = disciplinas_dict.get(allocation.disciplina)
        periodo = disciplina_obj.periodo if disciplina_obj else 1
        
        if periodo == 0:
            # This is an elective course
            allocations_eletivas.append(allocation)
        else:
            # Regular period course
            if periodo not in allocations_by_period:
                allocations_by_period[periodo] = []
            allocations_by_period[periodo].append(allocation)
    
    # Convert each period's allocations to PDF format
    for periodo, allocations in allocations_by_period.items():
        courses = []
        
        for allocation in allocations:
            # Group horarios by day to create slots
            horarios_by_day = {}
            for horario in allocation.horarios:
                day_key = day_mapping.get(horario.dia, horario.dia)
                if day_key not in horarios_by_day:
                    horarios_by_day[day_key] = []
                horarios_by_day[day_key].append(convert_horario_to_timeslot(horario))
            
            # Create slots list for this course
            slots = []
            for day, timeslots in horarios_by_day.items():
                # Sort timeslots to group consecutive ones properly
                timeslots.sort(key=lambda x: (x[0], int(x[1:])))  # Sort by shift then by number
                
                if len(timeslots) >= 2:
                    # Group consecutive slots (e.g., M1, M2 becomes ("Seg", "M1", "M2"))
                    i = 0
                    while i < len(timeslots):
                        start_slot = timeslots[i]
                        end_slot = start_slot
                        
                        # Find consecutive slots with same shift
                        j = i + 1
                        while j < len(timeslots):
                            current_shift = timeslots[j][0]
                            current_num = int(timeslots[j][1:])
                            end_shift = end_slot[0]
                            end_num = int(end_slot[1:])
                            
                            # Check if consecutive and same shift
                            if (current_shift == end_shift and 
                                current_num == end_num + 1):
                                end_slot = timeslots[j]
                                j += 1
                            else:
                                break
                        
                        slots.append((day, start_slot, end_slot))
                        i = j
                elif len(timeslots) == 1:
                    # Single slot
                    slot = timeslots[0]
                    slots.append((day, slot, slot))
            
            # Only add courses that have valid slots
            if slots:
                # Create course entry
                course_entry = {
                    "id": f"{periodo}_{allocation.disciplina.replace(' ', '_').replace(':', '').replace(',', '')}",
                    "name": allocation.disciplina,
                    "teacher": allocation.professor,
                    "slots": slots
                }
                courses.append(course_entry)
        
        periods_data[str(periodo)]["courses"] = courses
    
    # Process elective courses
    eletivas_courses = []
    for allocation in allocations_eletivas:
        # Group horarios by day to create slots
        horarios_by_day = {}
        for horario in allocation.horarios:
            day_key = day_mapping.get(horario.dia, horario.dia)
            if day_key not in horarios_by_day:
                horarios_by_day[day_key] = []
            horarios_by_day[day_key].append(convert_horario_to_timeslot(horario))
        
        # Create slots list for this course
        slots = []
        for day, timeslots in horarios_by_day.items():
            # Sort timeslots to group consecutive ones properly
            timeslots.sort(key=lambda x: (x[0], int(x[1:])))  # Sort by shift then by number
            
            if len(timeslots) >= 2:
                # Group consecutive slots (e.g., M1, M2 becomes ("Seg", "M1", "M2"))
                i = 0
                while i < len(timeslots):
                    start_slot = timeslots[i]
                    end_slot = start_slot
                    
                    # Find consecutive slots with same shift
                    j = i + 1
                    while j < len(timeslots):
                        current_shift = timeslots[j][0]
                        current_num = int(timeslots[j][1:])
                        end_shift = end_slot[0]
                        end_num = int(end_slot[1:])
                        
                        # Check if consecutive and same shift
                        if (current_shift == end_shift and 
                            current_num == end_num + 1):
                            end_slot = timeslots[j]
                            j += 1
                        else:
                            break
                    
                    slots.append((day, start_slot, end_slot))
                    i = j
            elif len(timeslots) == 1:
                # Single slot
                slot = timeslots[0]
                slots.append((day, slot, slot))
        
        # Only add courses that have valid slots
        if slots:
            # Create course entry for elective
            course_entry = {
                "id": f"ELET_{allocation.disciplina.replace(' ', '_').replace(':', '').replace(',', '')}",
                "name": allocation.disciplina,
                "teacher": allocation.professor,
                "slots": slots
            }
            eletivas_courses.append(course_entry)
    
    periods_data["Eletivas"]["courses"] = eletivas_courses
    
    return periods_data


# --- Main PDF Generation Logic ---
def create_timetable_pdf(use_genetic_algorithm=True):
    """Generates the complete PDF timetable."""
    global COURSE_DATA
    
    if use_genetic_algorithm:
        print("Running genetic algorithm to generate optimized schedule...")
        scheduler = GeneticScheduler()
        genetic_result = scheduler.executar_algoritmo(
            tamanho_populacao=30,
            num_geracoes=50
        )
        
        if genetic_result:
            print("Converting genetic algorithm result to PDF format...")
            COURSE_DATA = convert_genetic_algorithm_result_to_pdf_format(genetic_result)
        else:
            print("Genetic algorithm failed to find solution. Using mock data.")
            use_genetic_algorithm = False
    
    if not use_genetic_algorithm:
        print("Using mock data from schedule_data.py")
    
    c = canvas.Canvas(PDF_FILENAME, pagesize=landscape(A4))
    c.setTitle("Horário Escolar")

    # Course ID to Color mapping for Eletivas to keep color consistent if one spans pages (though current logic re-evaluates)
    eletivas_color_map = {} 

    # Process regular periods (1 to 8)
    for period_num_str in map(str, range(1, 9)):
        if period_num_str not in COURSE_DATA:
            print(f"Warning: Data for Period {period_num_str} not found. Skipping.")
            continue
        
        period_info = COURSE_DATA[period_num_str]
        draw_page_template(c, period_info["page_title"], period_info["location_info"])

        for course in period_info["courses"]:
            course_color = get_next_color() # Get a new color for each course instance for visual variety
            for day_str, start_slot, end_slot in course["slots"]:
                try:
                    day_idx = DAYS_OF_WEEK.index(day_str)
                except ValueError:
                    print(f"Warning: Invalid day '{day_str}' for course '{course['name']}'. Skipping slot.")
                    continue
                
                draw_course_block_split(c, day_idx, start_slot, end_slot,
                                      course["name"], course["teacher"], course_color)
        c.showPage()

    # Process "Eletivas" (elective courses with period = 0)
    if "Eletivas" in COURSE_DATA:
        eletivas_master_list = list(COURSE_DATA["Eletivas"]["courses"]) # Make a mutable copy
        eletivas_info = COURSE_DATA["Eletivas"]
        eletivas_page_count = 0

        # Assign persistent colors to Eletivas by ID if they need to be consistent across pages
        # For this version, a new color is picked if it gets replotted.
        # If consistency for a single Eletiva across multiple pages is vital, this needs adjustment.
        # For now, each attempt to plot an elective gets a fresh color from the palette.

        while eletivas_master_list:
            eletivas_page_count += 1
            page_title = eletivas_info["page_title_prefix"]
            if eletivas_page_count > 1:
                page_title += f" (Página {eletivas_page_count})"
            
            draw_page_template(c, page_title, eletivas_info["location_info"])
            
            # Stores (day_index, elementary_slot_column_index) for occupied slots on this page
            occupied_slots_on_this_page = set()
            
            processed_on_this_page_indices = [] # Store indices of courses from eletivas_master_list processed here

            for idx, course in enumerate(eletivas_master_list):
                can_place_course = True
                # Get all elementary slots this course would occupy
                prospective_slots_for_this_course = set()
                
                for day_str, start_slot, end_slot in course["slots"]:
                    try:
                        day_idx = DAYS_OF_WEEK.index(day_str)
                    except ValueError:
                        print(f"Warning: Invalid day '{day_str}' for Eletiva '{course['name']}'. Skipping slot.")
                        can_place_course = False; break 
                    
                    elementary_col_indices = get_elementary_slots_indices(start_slot, end_slot)
                    if not elementary_col_indices: # Error in slot definition
                         can_place_course = False; break

                    for col_idx in elementary_col_indices:
                        slot_tuple = (day_idx, col_idx)
                        if slot_tuple in occupied_slots_on_this_page:
                            can_place_course = False; break
                        prospective_slots_for_this_course.add(slot_tuple)
                    if not can_place_course: break
                
                if can_place_course:
                    # Place the course
                    course_color = eletivas_color_map.get(course['id'])
                    if not course_color:
                        course_color = get_next_color()
                        eletivas_color_map[course['id']] = course_color # Store for potential future use if needed

                    for day_str, start_slot, end_slot in course["slots"]:
                        day_idx = DAYS_OF_WEEK.index(day_str) # Already validated
                        draw_course_block_split(c, day_idx, start_slot, end_slot,
                                              course["name"], course["teacher"], course_color)
                    
                    # Mark its slots as occupied for this page
                    occupied_slots_on_this_page.update(prospective_slots_for_this_course)
                    processed_on_this_page_indices.append(idx)

            if not processed_on_this_page_indices and eletivas_master_list:
                 # This means no course could be placed on the current page,
                 # but there are still courses left. This could happen if remaining
                 # courses are too large or conflict inherently.
                 # For robustness, break to prevent infinite loops if no progress.
                 print(f"Warning: Could not place any more Eletivas on page {eletivas_page_count}. Remaining: {len(eletivas_master_list)}")
                 # You might want to list them or log them.
                 break


            # Remove placed courses from master list (iterate backwards to avoid index issues)
            for idx in sorted(processed_on_this_page_indices, reverse=True):
                eletivas_master_list.pop(idx)
            
            c.showPage()
            if not eletivas_master_list: # All done
                break
            if not processed_on_this_page_indices and eletivas_master_list: # No progress
                print("Stopping Eletivas processing due to no progress.")
                break


    c.save()
    print(f"PDF '{PDF_FILENAME}' generated successfully.")

if __name__ == '__main__':
    # You can set use_genetic_algorithm=False to use mock data instead
    create_timetable_pdf(use_genetic_algorithm=True)
