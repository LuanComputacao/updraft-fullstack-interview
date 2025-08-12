"""add-documents

Revision ID: e49b9875d4cb
Revises: f3b9c4319171
Create Date: 2025-07-12 17:45:22.321264

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = "e49b9875d4cb"
down_revision = "f3b9c4319171"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert sample document
    sample_document_content = """
    <h1><b>Rental Agreement - 2 Bedroom Apartment</b></h1>
    
    <p>This rental agreement is made between <b>Sunrise Properties LLC</b> (hereinafter referred to as "Landlord") and the tenant(s) for the property located at <b>123 Oak Street, Apartment 4B, Downtown District</b>.</p>
    
    <h2><b>Property Details:</b></h2>
    <ul>
        <li><b>Address:</b> 123 Oak Street, Apartment 4B</li>
        <li><b>Type:</b> 2 Bedroom, 1 Bathroom Apartment</li>
        <li><b>Square Footage:</b> 850 sq ft</li>
        <li><b>Floor:</b> 4th Floor</li>
        <li><b>Parking:</b> 1 assigned space included</li>
    </ul>
    
    <h2><b>Rental Terms:</b></h2>
    <ol>
        <li><b>Monthly Rent:</b> <i>$2,000</i> due on the 1st of each month</li>
        <li><b>Security Deposit:</b> <i>$2,000</i> (refundable upon move-out)</li>
        <li><b>Lease Term:</b> 12 months minimum</li>
        <li><b>Utilities:</b> Tenant responsible for electricity and internet</li>
        <li><b>Water/Sewer:</b> Included in rent</li>
    </ol>
    
    <h2><b>Apartment Features:</b></h2>
    <ul>
        <li>Modern kitchen with stainless steel appliances</li>
        <li>In-unit washer and dryer</li>
        <li>Central air conditioning and heating</li>
        <li>Large windows with city views</li>
        <li>Walk-in closet in master bedroom</li>
        <li>Balcony with outdoor space</li>
    </ul>
    
    <h2><b>Building Amenities:</b></h2>
    <ul>
        <li>24/7 doorman and security</li>
        <li>Fitness center access</li>
        <li>Rooftop terrace</li>
        <li>Package receiving service</li>
        <li>Bicycle storage</li>
    </ul>
    
    <h2><b>House Rules:</b></h2>
    <ol>
        <li>No smoking in the apartment or building</li>
        <li>Quiet hours from 10 PM to 8 AM</li>
        <li>Maximum 2 occupants per bedroom</li>
        <li>No pets without written approval</li>
        <li>Tenant must maintain renters insurance</li>
    </ol>
    
    <h2><b>Contact Information:</b></h2>
    <p>For maintenance requests or questions, contact:</p>
    <ul>
        <li><b>Property Manager:</b> <span>Sarah Johnson</span></li>
        <li><b>Phone:</b> <span>(555) 123-4567</span></li>
        <li><b>Email:</b> <span>sarah.johnson@sunriseproperties.com</span></li>
        <li><b>Emergency Maintenance:</b> <span>(555) 999-8888</span></li>
    </ul>
    
    <h2><b>Move-in Requirements:</b></h2>
    <ol>
        <li>First month's rent and security deposit</li>
        <li>Completed rental application</li>
        <li>Proof of income (3x monthly rent)</li>
        <li>Credit check and background screening</li>
        <li>Renters insurance certificate</li>
    </ol>
    
    <p>This apartment offers the perfect balance of comfort and convenience in a prime downtown location. The building is well-maintained and offers excellent amenities for modern living.</p>
    """

    # Insert the sample document
    op.execute(
        text(
            """
        INSERT INTO documents (id, title, content_html, created_at) 
        VALUES ('550e8400-e29b-41d4-a716-446655440000', 'Downtown 2BR Apartment Rental Agreement', :content_html, NOW())
    """
        ).bindparams(content_html=sample_document_content.strip())
    )


def downgrade() -> None:
    # Remove the sample document
    op.execute(
        text("DELETE FROM documents WHERE id = '550e8400-e29b-41d4-a716-446655440000'")
    )
