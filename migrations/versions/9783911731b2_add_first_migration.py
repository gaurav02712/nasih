"""Add first migration

Revision ID: 9783911731b2
Revises: 
Create Date: 2020-04-23 16:49:35.149947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9783911731b2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currency',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('country', sa.String(length=45), nullable=False),
    sa.Column('currency', sa.String(length=45), nullable=False),
    sa.Column('code', sa.String(length=45), nullable=False),
    sa.Column('symbol', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hotel',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('iata_code',
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=90), nullable=False),
    sa.Column('city', sa.String(length=45), nullable=True),
    sa.Column('country', sa.String(length=45), nullable=False),
    sa.Column('iata', sa.String(length=4), nullable=False),
    sa.Column('iaco', sa.String(length=9), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('timezone', sa.String(length=45), nullable=False),
    sa.Column('dst', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('question', sa.String(length=250), nullable=False),
    sa.Column('question_html', sa.String(length=250), nullable=True),
    sa.Column('is_single_choice', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('f_name', sa.String(length=45), nullable=False),
    sa.Column('l_name', sa.String(length=45), nullable=False),
    sa.Column('email', sa.String(length=45), nullable=False),
    sa.Column('password', sa.String(length=355), nullable=True),
    sa.Column('username', sa.String(length=45), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('is_varified', sa.Integer(), nullable=False),
    sa.Column('social_id', sa.String(length=50), nullable=True),
    sa.Column('register_by', sa.String(length=50), nullable=True),
    sa.Column('profile_image_url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('booking',
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('booking_id', sa.String(length=45), nullable=False),
    sa.Column('providerConfirmationId', sa.String(length=45), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('hotel_name', sa.String(length=45), nullable=False),
    sa.Column('checking_date', sa.DateTime(), nullable=False),
    sa.Column('checkout_date', sa.DateTime(), nullable=False),
    sa.Column('number_of_guest', sa.Integer(), nullable=False),
    sa.Column('number_of_room', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=30), nullable=False),
    sa.Column('address', sa.String(length=45), nullable=False),
    sa.Column('booking_status', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('device_info',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('device_id', sa.String(length=255), nullable=True),
    sa.Column('os_type', sa.String(length=10), nullable=True),
    sa.Column('os_version', sa.String(length=10), nullable=True),
    sa.Column('app_version', sa.String(length=10), nullable=True),
    sa.Column('build_version', sa.String(length=10), nullable=True),
    sa.Column('model_name', sa.String(length=255), nullable=True),
    sa.Column('model_number', sa.String(length=255), nullable=True),
    sa.Column('fcm_token', sa.String(length=512), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fav_entity',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('entity_id', sa.String(length=45), nullable=False),
    sa.Column('entity_type', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fav_entity_user_id'), 'fav_entity', ['user_id'], unique=False)
    op.create_table('notification',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('body', sa.String(length=250), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('is_seen', sa.Boolean(), nullable=False),
    sa.Column('is_viewed', sa.Boolean(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('question_option',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('option', sa.String(length=80), nullable=False),
    sa.Column('option_icon', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_type', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('user_token',
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('token', sa.String(length=1000), nullable=False),
    sa.Column('refresh_token', sa.String(length=1000), nullable=False),
    sa.Column('expired_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('refresh_token'),
    sa.UniqueConstraint('token')
    )
    op.create_table('user_question_releation',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['answer_id'], ['question_option.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_question_releation')
    op.drop_table('user_token')
    op.drop_table('user_role')
    op.drop_table('question_option')
    op.drop_table('notification')
    op.drop_index(op.f('ix_fav_entity_user_id'), table_name='fav_entity')
    op.drop_table('fav_entity')
    op.drop_table('device_info')
    op.drop_table('booking')
    op.drop_table('user')
    op.drop_table('question')
    op.drop_table('iata_code')
    op.drop_table('hotel')
    op.drop_table('currency')
    # ### end Alembic commands ###
