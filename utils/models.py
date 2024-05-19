# from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from PIL import Image
# import io
#
# DATABASE_URL = "postgresql+psycopg2://user:password@localhost/object_detection_db"
#
# engine = create_engine(
#     DATABASE_URL,
#     isolation_level="SERIALIZABLE",
# )
# Session = sessionmaker(bind=engine)
# Base = declarative_base()
#
#
# class ImageModel(Base):
#     __tablename__ = 'images'
#
#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String, index=True)
#     image_data = Column(LargeBinary)
#
#
# Base.metadata.create_all(bind=engine)
#
#
# def save_image_to_db(filename, image):
#     session = Session()
#     img_byte_arr = io.BytesIO()
#     image.save(img_byte_arr, format='PNG')
#     img_byte_arr = img_byte_arr.getvalue()
#
#     img = ImageModel(filename=filename, image_data=img_byte_arr)
#     session.add(img)
#     session.commit()
#     session.close()
#
#
# def load_image_from_db(image_id):
#     session = Session()
#     img = session.query(ImageModel).filter_by(id=image_id).first()
#     session.close()
#     if img is not None:
#         img_byte_arr = io.BytesIO(img.image_data)
#         image = Image.open(img_byte_arr)
#         return image
#     return None
