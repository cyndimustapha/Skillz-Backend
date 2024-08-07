"""Initial migration.

Revision ID: 82964b9fb805
Revises: 
Create Date: 2024-08-05 12:11:44.660387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82964b9fb805'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('profile_picture', sa.String(length=255), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('instructor_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['instructor_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('receiver_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('sent_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coursecontent',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('content_type', sa.String(length=50), nullable=True),
    sa.Column('content_url', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('enrollments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('learner_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('enrolled_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('completed_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['learner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('learner_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('payment_status', sa.String(length=50), nullable=True),
    sa.Column('payment_date', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['learner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('learner_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['learner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('accolades',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('enrollment_id', sa.Integer(), nullable=False),
    sa.Column('accolade_type', sa.String(length=100), nullable=True),
    sa.Column('awarded_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['enrollment_id'], ['enrollments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accolades')
    op.drop_table('reviews')
    op.drop_table('payments')
    op.drop_table('enrollments')
    op.drop_table('coursecontent')
    op.drop_table('messages')
    op.drop_table('courses')
    op.drop_table('users')
    # ### end Alembic commands ###
